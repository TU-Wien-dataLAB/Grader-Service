// token: 0b79bab50daca910b000d4f1a2b675d604257e42

import { Lecture } from "../model/lecture";

export enum Scope {
  student = 0,
  tutor = 1,
  instructor = 2,
  admin = 3,
}

interface PermissionScopes {
  [lecture_code: string]: Scope;
}

export namespace UserPermissions {
  let permissions: PermissionScopes = null;

  export function getScope(lecture: Lecture) {
    if (permissions == null) {
      // TODO: set permissions using API call
    }
    return permissions[lecture.code]
  }
}