import datetime
import json
import os
import time
from urllib.parse import urlparse
from grader_service.orm.assignment import Assignment
from grader_service.orm.lecture import Lecture
from grader_service.orm.submission import Submission
import jwt
from traitlets import Callable, Dict, Unicode, Union
from traitlets.config import SingletonConfigurable
from http import HTTPStatus
from tornado.escape import url_escape, json_decode
from tornado.httpclient import AsyncHTTPClient, HTTPClientError, HTTPRequest
from tornado.web import HTTPError

def default_lti_username_convert(username: str) -> str:
    return username

def default_enable_lti(lecture, assignment, submissions):
    return {"enable_lti": False, "sync_on_feedback": False}

class LTISyncGrades(SingletonConfigurable):
    enable_lti_features = Union(
        [Dict({"enable_lti": False, "sync_on_feedback": False}),
         Callable(default_enable_lti)],
        allow_none=True,
        config=True,
        help="""
        Determines if the LTI plugin should be used, defaults to False.
        Is either a dictionary containing the keys "enable_lti":bool and "sync_on_feedback":bool or
        a function returning a dict with these keys.
        """,
    )
    client_id = Unicode(None, config=True, allow_none=True)
    token_url = Unicode(None, config=True, allow_none=True)
    # function used to change the hub username to the lti sourcedid value
    help_msg = "Converts the grader service username to the lti sourced id."
    username_convert = Callable(default_value=default_lti_username_convert,
                                         config=True,
                                         allow_none=True,
                                         help=help_msg)
    token_private_key = Union(
        [Unicode(os.environ.get('LTI_PRIVATE_KEY', None)),
         Callable(None)],
        allow_none=True,
        config=True,
        help="""
        Private Key used to encrypt bearer token request
        """,
    )
    resolve_lti_urls = Callable(default_value=None,
                                         config=True,
                                         allow_none=False,
                                         help="Returns membership and lineitem URL needed for grade sync")

    # cache for lti token    
    cache_token = {"token": None, "ttl": datetime.datetime.now()}
    
    def check_if_lti_enabled(self, lecture, assignment, submissions, sync_on_feedback):
        if callable(self.enable_lti_features):
            enable_lti = self.enable_lti_features(lecture, assignment, submissions)
        else:
            enable_lti = self.enable_lti_features
        
        if enable_lti["enable_lti"]:
            if sync_on_feedback:
                if enable_lti["sync_on_feedback"]:
                    return True
                else: 
                    return False
            else:
                return True
        else:
            return False
            
    async def start(self, lecture: dict, assignment: dict, submissions: list[dict]):

        # # Check if the LTI plugin should be used
        # if not self._check_if_lti_enabled(lecture, assignment, submissions, sync_on_feedback):
        #     self.log.info("Skipping LTI plugin as it is not enabled")
        #     return {"syncable_users": 0, "synced_user": 0}
        
        self.log.info("Start LTI Grade Sync")

        # 1. request bearer token
        stamp = datetime.datetime.now()
        if self.cache_token["token"] and self.cache_token["ttl"] > stamp - datetime.timedelta(
                minutes=50):
            token = self.cache_token["token"]
        else:
            token = await self.request_bearer_token()
            self.cache_token["token"] = token
            self.cache_token["ttl"] = datetime.datetime.now()

        # 2. resolve lti urls
        try:
            lti_urls = self.resolve_lti_urls(lecture, assignment, submissions)
            lineitems_url = lti_urls["lineitems_url"]
            membership_url = lti_urls["membership_url"]
        except Exception as e:
            self.log.error(e)
            return
        # 3. get all members
        httpclient = AsyncHTTPClient()
        try:
            response = await httpclient.fetch(HTTPRequest(url=membership_url, method="GET",
                                                          headers={
                                                            "Authorization": "Bearer " + self.cache_token["token"],
                                                            "Accept": "application/vnd.ims.lti-nrps.v2.membershipcontainer+json"}))
        except HTTPClientError as e:
            self.log.error(e.response)
            raise HTTPError(e.code, reason="Unable to get users of course:" + e.response.reason)
        members = json_decode(response.body)["members"]
    
        # 4. match usernames of submissions to lti memberships
        # and generate for each submission a request body -> grades list
        grades = []
        syncable_user_count = 0
        for submission in submissions:
            for member in members:
                if member["lis_person_sourcedid"] == self.username_convert(submission["username"]):
                    syncable_user_count += 1
                    grades.append(self.build_grade_publish_body(member["user_id"], submission["score"],
                                                           float(assignment["points"])))
        # 6. get all lineitems
        try:
            response = await httpclient.fetch(HTTPRequest(url=lineitems_url, method="GET",
                                                          headers={
                                                            "Authorization": "Bearer " + self.cache_token["token"],
                                                            "Accept": "application/vnd.ims.lis.v2.lineitemcontainer+json"}))
        except HTTPClientError as e:
            self.log.error(e.response)
            raise HTTPError(e.code, reason="Unable to get lineitems of course:" + e.response.reason)
        lineitems = json_decode(response.body)
        
        # 7. check if a lineitem with assignment name exists
        lineitem = None
        for item in lineitems:
            if item["label"] == assignment["name"]:
                # lineitem found
                lineitem = item
                break
        
        # 8. if not create a lineitem with the assignment name
        if lineitem is None:
            lineitem_body = {"scoreMaximum": float(assignment["points"]), "label": assignment["name"],
                             "resourceId": assignment["id"],
                             "tag": "grade", "startDateTime": str(datetime.datetime.now()),
                             "endDateTime": str(datetime.date.today() + datetime.timedelta(days=1, hours=1))}
            try:
                response = await httpclient.fetch(HTTPRequest(url=lineitems_url, method="POST", body=json.dumps(lineitem_body),
                                                          headers={
                                                            "Authorization": "Bearer " + self.cache_token["token"],
                                                            "Content-Type": "application/vnd.ims.lis.v2.lineitem+json"}))
            except HTTPClientError as e:
                self.log.error(e.response)
                raise HTTPError(e.code, reason="Unable to create new lineitem in course:" + e.response.reason)
        lineitem = json_decode(response.body)[0]
        
        # 9. push grades to lineitem
        url_parsed = urlparse(lineitem["id"])
        lineitem = url_parsed._replace(path=url_parsed.path + "/scores").geturl()
        
        synced_user = 0
        for grade in grades:
            try:
                response = await httpclient.fetch(HTTPRequest(url=lineitem, method="POST", body=json.dumps(grade),
                                                          headers={
                                                            "Authorization": "Bearer " + self.cache_token["token"],
                                                            "Content-Type": "application/vnd.ims.lis.v1.score+json"}))
                synced_user += 1
            except HTTPClientError as e:
                self.log.error(e.response)
        self.log.info("LTI Grade Sync finished successfully")
        return {"syncable_users": syncable_user_count, "synced_user": synced_user}

    
    def build_grade_publish_body(self, uid: str, score: float, max_score: float):
        return {
            "timestamp": str(datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()),
            "scoreGiven": score,
            "comment": "Automatically synced",
            "scoreMaximum": max_score,
            "activityProgress": "Submitted",
            "gradingProgress": "FullyGraded",
            "userId": uid
        }
    
    async def request_bearer_token(self):
        # get config variables
        if self.client_id is None:
            raise HTTPError(HTTPStatus.NOT_FOUND,
                            reason="Unable to request bearer token: client_id is not set in grader config")
        if self.token_url is None:
            raise HTTPError(HTTPStatus.NOT_FOUND,
                            reason="Unable to request bearer token: token_url is not set in grader config")

        private_key = self.token_private_key
        if private_key is None:
            raise HTTPError(HTTPStatus.NOT_FOUND,
                            reason="Unable to request bearer token: token_private_key is not set in grader config")
        if callable(private_key):
            private_key = private_key()

        payload = {"iss": "grader-service", "sub": self.client_id, "aud": [self.token_url],
                   "ist": str(int(time.time())), "exp": str(int(time.time()) + 60),
                   "jti": str(int(time.time())) + "123"}
        try:
            encoded = jwt.encode(payload, private_key, algorithm="RS256")
        except Exception as e:
            raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY, f"Unable to encode payload: {str(e)}")
        self.log.info("encoded: " + encoded)
        scopes = [
            "https://purl.imsglobal.org/spec/lti-ags/scope/score",
            "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem",
            "https://purl.imsglobal.org/spec/lti-nrps/scope/contextmembership.readonly"
        ]
        scopes = url_escape(" ".join(scopes))
        data = f"grant_type=client_credentials&client_assertion_type=urn%3Aietf%3Aparams%3Aoauth%3Aclient-assertion" \
               f"-type%3Ajwt-bearer&client_assertion={encoded}&scope={scopes} "
        self.log.info("data: " + data)

        httpclient = AsyncHTTPClient()
        try:
            response = await httpclient.fetch(HTTPRequest(url=self.token_url, method="POST", body=data,
                                                          headers={
                                                              "Content-Type": "application/x-www-form-urlencoded"}))
        except HTTPClientError as e:
            self.log.error(e.response)
            raise HTTPError(e.code, reason="Unable to request token:" + e.response.reason)
        return json_decode(response.body)["access_token"]