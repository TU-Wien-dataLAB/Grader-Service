(self["webpackChunkgrading"] = self["webpackChunkgrading"] || []).push([["lib_index_js-webpack_sharing_consume_default_jupyterlab_statedb-webpack_sharing_consume_defau-d707a1"],{

/***/ "./lib/components/assignments/assignment-list.component.js":
/*!*****************************************************************!*\
  !*** ./lib/components/assignments/assignment-list.component.js ***!
  \*****************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "AssignmentsComponent": () => (/* binding */ AssignmentsComponent)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _services_assignments_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/assignments.service */ "./lib/services/assignments.service.js");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _assignment_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./assignment.component */ "./lib/components/assignments/assignment.component.js");
/* harmony import */ var _blueprintjs_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @blueprintjs/core */ "webpack/sharing/consume/default/@blueprintjs/core/@blueprintjs/core");
/* harmony import */ var _blueprintjs_core__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _blueprintjs_icons__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @blueprintjs/icons */ "webpack/sharing/consume/default/@blueprintjs/icons/@blueprintjs/icons");
/* harmony import */ var _blueprintjs_icons__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_blueprintjs_icons__WEBPACK_IMPORTED_MODULE_3__);






class AssignmentsComponent extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.state = {
            isOpen: false,
            assignments: new Array()
        };
        this.toggleOpen = () => {
            this.setState({ isOpen: !this.state.isOpen });
        };
        this.lecture = props.lecture;
        this.state.isOpen = props.open || false;
    }
    componentDidMount() {
        (0,_services_assignments_service__WEBPACK_IMPORTED_MODULE_4__.getAllAssignments)(this.lecture.id).subscribe(assignments => {
            this.setState(this.state.assignments = assignments);
        });
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "AssignmentsComponent" },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { onClick: this.toggleOpen, className: "collapse-header" },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_2__.Icon, { icon: _blueprintjs_icons__WEBPACK_IMPORTED_MODULE_3__.IconNames.LEARNING, className: "flavor-icon" }),
                this.lecture.name,
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_2__.Icon, { iconSize: _blueprintjs_core__WEBPACK_IMPORTED_MODULE_2__.Icon.SIZE_LARGE, icon: _blueprintjs_icons__WEBPACK_IMPORTED_MODULE_3__.IconNames.CHEVRON_DOWN, className: `collapse-icon ${this.state.isOpen ? "collapse-icon-open" : ""}` })),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.Collapse, { isOpen: this.state.isOpen, className: "collapse-body", transitionDuration: 300, keepChildrenMounted: true },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("ul", null, this.state.assignments.map((el, index) => react__WEBPACK_IMPORTED_MODULE_0__.createElement(_assignment_component__WEBPACK_IMPORTED_MODULE_5__.AssignmentComponent, { index: index, lecture: this.lecture, assignment: el })))));
    }
}


/***/ }),

/***/ "./lib/components/assignments/assignment.component.js":
/*!************************************************************!*\
  !*** ./lib/components/assignments/assignment.component.js ***!
  \************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "AssignmentComponent": () => (/* binding */ AssignmentComponent)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _blueprintjs_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @blueprintjs/core */ "webpack/sharing/consume/default/@blueprintjs/core/@blueprintjs/core");
/* harmony import */ var _blueprintjs_core__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _blueprintjs_icons__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @blueprintjs/icons */ "webpack/sharing/consume/default/@blueprintjs/icons/@blueprintjs/icons");
/* harmony import */ var _blueprintjs_icons__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_blueprintjs_icons__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _index__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../index */ "./lib/index.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _services_submissions_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/submissions.service */ "./lib/services/submissions.service.js");
/* harmony import */ var _services_assignments_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/assignments.service */ "./lib/services/assignments.service.js");







class AssignmentComponent extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.iconSize = 14;
        this.state = {
            filesOpen: false,
            submissionsOpen: true,
            submissions: new Array()
        };
        this.toggleOpen = (collapsable) => {
            if (collapsable == "files") {
                this.setState({ filesOpen: !this.state.filesOpen });
            }
            else if (collapsable == "submissions") {
                this.setState({ submissionsOpen: !this.state.submissionsOpen });
            }
        };
        this.assignment = props.assignment;
        this.index = props.index;
        this.lecture = props.lecture;
        this.toggleOpen = this.toggleOpen.bind(this);
        this.openFile = this.openFile.bind(this);
        this.fetchAssignment = this.fetchAssignment.bind(this);
        this.submitAssignment = this.submitAssignment.bind(this);
        this.getSubmissions = this.getSubmissions.bind(this);
    }
    componentDidMount() {
        this.getSubmissions();
    }
    async openFile(path) {
        if (this.assignment.status == 'released') { // if not fetched
            let result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.showDialog)({
                title: "Assignment not fetched yet!",
                body: "Before working on assignments you need to fetch them! Do you want to fetch the assignment now?",
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.Dialog.okButton({ label: "Fetch Now" })]
            });
            if (!result.button.accept) {
                return;
            }
            else {
                await this.fetchAssignment();
            }
        }
        console.log("Opening file: " + path);
        _index__WEBPACK_IMPORTED_MODULE_4__.GlobalObjects.commands.execute('docmanager:open', {
            path: path,
            options: {
                mode: 'tab-after' // tab-after tab-before split-bottom split-right split-left split-top
            }
        }).catch(error => {
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.showErrorMessage)("Error Opening File", error);
        });
    }
    async fetchAssignment() {
        try {
            let result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.showDialog)({
                title: "Fetch Assignment",
                body: `Do you want to fetch ${this.assignment.name}?`,
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.Dialog.okButton({ label: "Fetch" })]
            });
            if (result.button.accept) {
                // update assignment
                this.assignment = await (0,_services_assignments_service__WEBPACK_IMPORTED_MODULE_5__.fetchAssignment)(this.lecture.id, this.assignment.id).toPromise();
            }
        }
        catch (e) {
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.showErrorMessage)("Error Fetching Assignment", e);
        }
    }
    async submitAssignment() {
        try {
            let result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.showDialog)({
                title: "Submit Assignment",
                body: `Do you want to submit ${this.assignment.name}? You can always re-submit the assignment before the due date.`,
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.Dialog.okButton({ label: "Submit" })],
            });
            if (result.button.accept) {
                await (0,_services_submissions_service__WEBPACK_IMPORTED_MODULE_6__.submitAssignment)(this.lecture, this.assignment).toPromise();
                await this.getSubmissions();
            }
        }
        catch (e) {
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.showErrorMessage)("Error Submitting Assignment", e);
        }
    }
    getSubmissions() {
        (0,_services_submissions_service__WEBPACK_IMPORTED_MODULE_6__.getSubmissions)(this.lecture, this.assignment).subscribe(userSubmissions => this.setState({ submissions: userSubmissions.submissions }), error => (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.showErrorMessage)("Error Loading Submissions", error));
    }
    render() {
        // TODO: show due date of assignment
        return react__WEBPACK_IMPORTED_MODULE_0__.createElement("li", { key: this.index },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "assignment" },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "assignment-header" },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_1__.Icon, { icon: _blueprintjs_icons__WEBPACK_IMPORTED_MODULE_2__.IconNames.INBOX, iconSize: this.iconSize, className: "flavor-icon" }),
                    this.assignment.name,
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { className: "button-list" },
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_1__.Button, { className: "assignment-button", onClick: this.fetchAssignment, icon: _blueprintjs_icons__WEBPACK_IMPORTED_MODULE_2__.IconNames.CLOUD_DOWNLOAD, disabled: this.assignment.status != "released", outlined: true, intent: _blueprintjs_core__WEBPACK_IMPORTED_MODULE_1__.Intent.PRIMARY }, "Fetch"),
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_1__.Button, { className: "assignment-button", onClick: this.submitAssignment, icon: _blueprintjs_icons__WEBPACK_IMPORTED_MODULE_2__.IconNames.SEND_MESSAGE, disabled: this.assignment.status != "fetched", outlined: true, intent: _blueprintjs_core__WEBPACK_IMPORTED_MODULE_1__.Intent.SUCCESS }, "Submit"))),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { onClick: () => this.toggleOpen("files"), className: "assignment-title" },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_1__.Icon, { icon: _blueprintjs_icons__WEBPACK_IMPORTED_MODULE_2__.IconNames.CHEVRON_RIGHT, iconSize: this.iconSize, className: `collapse-icon-small ${this.state.filesOpen ? "collapse-icon-small-open" : ""}` }),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_1__.Icon, { icon: _blueprintjs_icons__WEBPACK_IMPORTED_MODULE_2__.IconNames.FOLDER_CLOSE, iconSize: this.iconSize, className: "flavor-icon" }),
                    "Exercises and Files"),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_1__.Collapse, { isOpen: this.state.filesOpen },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "assignment-content" },
                        this.assignment.exercises.map((ex, i) => react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "list-element", onClick: () => this.openFile(`${this.lecture.name}/${this.assignment.name}/${ex.name}`) },
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_1__.Icon, { icon: _blueprintjs_icons__WEBPACK_IMPORTED_MODULE_2__.IconNames.EDIT, iconSize: this.iconSize, className: "flavor-icon" }),
                            ex.name)),
                        this.assignment.files.map((file, i) => react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "list-element", onClick: () => this.openFile(`${this.lecture.name}/${this.assignment.name}/${file.name}`) },
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_1__.Icon, { icon: _blueprintjs_icons__WEBPACK_IMPORTED_MODULE_2__.IconNames.DOCUMENT, iconSize: this.iconSize, className: "flavor-icon" }),
                            file.name)))),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { onClick: () => this.toggleOpen("submissions"), className: "assignment-title" },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_1__.Icon, { icon: _blueprintjs_icons__WEBPACK_IMPORTED_MODULE_2__.IconNames.CHEVRON_RIGHT, iconSize: this.iconSize, className: `collapse-icon-small ${this.state.submissionsOpen ? "collapse-icon-small-open" : ""}` }),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_1__.Icon, { icon: _blueprintjs_icons__WEBPACK_IMPORTED_MODULE_2__.IconNames.TICK_CIRCLE, iconSize: this.iconSize, className: "flavor-icon" }),
                    "Submissions"),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_1__.Collapse, { isOpen: this.state.submissionsOpen },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "assignment-content" }, this.state.submissions.map((submission, i) => react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "submission-element" },
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_1__.Icon, { icon: _blueprintjs_icons__WEBPACK_IMPORTED_MODULE_2__.IconNames.FORM, iconSize: this.iconSize, className: "flavor-icon" }),
                        submission.submitted_at,
                        submission.status != "not_graded" ?
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_1__.Button, { className: "assignment-button", icon: _blueprintjs_icons__WEBPACK_IMPORTED_MODULE_2__.IconNames.CLOUD_DOWNLOAD, active: true, outlined: true, intent: _blueprintjs_core__WEBPACK_IMPORTED_MODULE_1__.Intent.PRIMARY, small: true }, "Fetch Feedback")
                            : null))))));
    }
}


/***/ }),

/***/ "./lib/components/assignments/courses.component.js":
/*!*********************************************************!*\
  !*** ./lib/components/assignments/courses.component.js ***!
  \*********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CoursesComponent": () => (/* binding */ CoursesComponent)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _assignment_list_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./assignment-list.component */ "./lib/components/assignments/assignment-list.component.js");
/* harmony import */ var _services_lectures_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../services/lectures.service */ "./lib/services/lectures.service.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);




class CoursesComponent extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.state = {
            lectures: new Array()
        };
        // this.state = {"lectures": props.lectures};
    }
    componentDidMount() {
        (0,_services_lectures_service__WEBPACK_IMPORTED_MODULE_2__.getAllLectures)().subscribe(lectures => this.setState(this.state.lectures = lectures), error => (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)("Error Fetching Lectures", error));
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "course-list" }, this.state.lectures.map((el, index) => react__WEBPACK_IMPORTED_MODULE_0__.createElement(_assignment_list_component__WEBPACK_IMPORTED_MODULE_3__.AssignmentsComponent, { lecture: el, open: index == 0 })));
    }
}


/***/ }),

/***/ "./lib/components/coursemanage/coursemanage.component.js":
/*!***************************************************************!*\
  !*** ./lib/components/coursemanage/coursemanage.component.js ***!
  \***************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CourseManageComponent": () => (/* binding */ CourseManageComponent)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _services_lectures_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../services/lectures.service */ "./lib/services/lectures.service.js");
/* harmony import */ var _coursemanageassignment_list_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./coursemanageassignment-list.component */ "./lib/components/coursemanage/coursemanageassignment-list.component.js");



class CourseManageComponent extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.state = {
            lectures: new Array()
        };
        // this.state = {"lectures": props.lectures};
    }
    componentDidMount() {
        (0,_services_lectures_service__WEBPACK_IMPORTED_MODULE_1__.getAllLectures)().subscribe(lectures => {
            console.log(lectures);
            this.setState(this.state.lectures = lectures);
        });
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "course-list" }, this.state.lectures.map((el, index) => react__WEBPACK_IMPORTED_MODULE_0__.createElement(_coursemanageassignment_list_component__WEBPACK_IMPORTED_MODULE_2__.CourseManageAssignmentsComponent, { lecture: el, title: el.name, open: index == 0 })));
    }
}


/***/ }),

/***/ "./lib/components/coursemanage/coursemanageassignment-list.component.js":
/*!******************************************************************************!*\
  !*** ./lib/components/coursemanage/coursemanageassignment-list.component.js ***!
  \******************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CourseManageAssignmentsComponent": () => (/* binding */ CourseManageAssignmentsComponent)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _services_assignments_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/assignments.service */ "./lib/services/assignments.service.js");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _coursemanageassignment_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./coursemanageassignment.component */ "./lib/components/coursemanage/coursemanageassignment.component.js");
/* harmony import */ var _blueprintjs_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @blueprintjs/core */ "webpack/sharing/consume/default/@blueprintjs/core/@blueprintjs/core");
/* harmony import */ var _blueprintjs_core__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_apputils_lib_dialog__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/apputils/lib/dialog */ "./node_modules/@jupyterlab/apputils/lib/dialog.js");
/* harmony import */ var _jupyterlab_apputils_lib_inputdialog__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/apputils/lib/inputdialog */ "./node_modules/@jupyterlab/apputils/lib/inputdialog.js");







class CourseManageAssignmentsComponent extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.state = {
            isOpen: false,
            assignments: new Array()
        };
        this.toggleOpen = () => {
            this.setState({ isOpen: !this.state.isOpen });
        };
        this.title = props.title;
        this.lecture = props.lecture;
        this.state.isOpen = props.open || false;
        this.getAssignments = this.getAssignments.bind(this);
    }
    async createAssignment() {
        try {
            let name;
            _jupyterlab_apputils_lib_inputdialog__WEBPACK_IMPORTED_MODULE_3__.InputDialog.getText({ title: 'Input assignment name' }).then(input => {
                name = input;
            });
            (0,_services_assignments_service__WEBPACK_IMPORTED_MODULE_4__.createAssignment)(this.lecture.id, name);
        }
        catch (e) {
            (0,_jupyterlab_apputils_lib_dialog__WEBPACK_IMPORTED_MODULE_5__.showErrorMessage)("Error Creating Assignment", e);
        }
    }
    componentDidMount() {
        this.getAssignments();
    }
    getAssignments() {
        (0,_services_assignments_service__WEBPACK_IMPORTED_MODULE_4__.getAllAssignments)(this.lecture.id).subscribe(assignments => {
            console.log(assignments);
            this.setState(this.state.assignments = assignments);
        });
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "CourseManageAssignmentsComponent" },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { onClick: this.toggleOpen, className: "collapse-header" },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_2__.Icon, { icon: "learning", className: "flavor-icon" }),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_2__.Icon, { icon: "chevron-down", className: `collapse-icon ${this.state.isOpen ? "collapse-icon-open" : ""}` }),
                this.title),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.Collapse, { isOpen: this.state.isOpen, className: "collapse-body", keepChildrenMounted: true },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("ul", null, this.state.assignments.map((el, index) => react__WEBPACK_IMPORTED_MODULE_0__.createElement(_coursemanageassignment_component__WEBPACK_IMPORTED_MODULE_6__.CourseManageAssignmentComponent, { index: index, lectureName: this.title, lecture: this.lecture, assignment: el }))),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "assignment-create" },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_2__.Button, { icon: "add", outlined: true, onClick: this.createAssignment, className: "assignment-button" }, "Create new Assignment"))));
    }
}


/***/ }),

/***/ "./lib/components/coursemanage/coursemanageassignment.component.js":
/*!*************************************************************************!*\
  !*** ./lib/components/coursemanage/coursemanageassignment.component.js ***!
  \*************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CourseManageAssignmentComponent": () => (/* binding */ CourseManageAssignmentComponent)
/* harmony export */ });
/* harmony import */ var _blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @blueprintjs/core */ "webpack/sharing/consume/default/@blueprintjs/core/@blueprintjs/core");
/* harmony import */ var _blueprintjs_core__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _index__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../index */ "./lib/index.js");
/* harmony import */ var _services_submissions_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../services/submissions.service */ "./lib/services/submissions.service.js");





class CourseManageAssignmentComponent extends react__WEBPACK_IMPORTED_MODULE_2__.Component {
    constructor(props) {
        super(props);
        this.iconSize = 14;
        this.state = {
            isOpen: false,
            submissions: new Array(),
        };
        this.toggleOpen = () => {
            console.log("toggle assignment header");
            this.setState({ isOpen: !this.state.isOpen });
        };
        this.assignment = props.assignment;
        this.index = props.index;
        this.lectureName = props.lectureName;
        this.lecture = props.lecture;
    }
    componentDidMount() {
        // TODO: should only get all submissions if assignment is released
        (0,_services_submissions_service__WEBPACK_IMPORTED_MODULE_3__.getSubmissions)(this.lecture, { id: this.index }).subscribe(userSubmissions => {
            console.log(userSubmissions);
            this.setState(this.state.submissions = userSubmissions.submissions);
        });
    }
    openFile(path) {
        console.log("Opening file: " + path);
        _index__WEBPACK_IMPORTED_MODULE_4__.GlobalObjects.commands.execute('docmanager:open', {
            path: path,
            options: {
                mode: 'tab-after' // tab-after tab-before split-bottom split-right split-left split-top
            }
        }).catch(error => {
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)("Error Opening File", error);
        });
    }
    openGrading(lectureID, assignmentID) {
        _index__WEBPACK_IMPORTED_MODULE_4__.GlobalObjects.commands.execute('grading:open', {
            lectureID,
            assignmentID
        }).catch(error => {
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)("Error Opening Submission View", error);
        });
    }
    async openPreview() {
        //TODO: This should open the file in the preview directory not the /lecture/assignment directory
        let names = this.assignment.exercises.map(ex => ex.name);
        let path = `${this.lecture.name}/${this.assignment.name}/`;
        if (names.length > 1) {
            let value = await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.InputDialog.getItem({
                title: 'Choose an exercise to preview',
                items: names
            });
            if (value.value == null)
                return;
            path += value.value;
        }
        else {
            path += this.assignment.exercises[0].name;
        }
        _index__WEBPACK_IMPORTED_MODULE_4__.GlobalObjects.commands.execute('docmanager:open', {
            path: path,
            options: {
                mode: 'split-right' // tab-after tab-before split-bottom split-right split-left split-top
            }
        }).catch(error => {
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)("Error Opening File", error);
        });
    }
    async pushAssignment() {
        let result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
            title: "Push Assignment",
            body: `Do you want to push ${this.assignment.name}? This updates the state of the assignment on the server with your local state.`,
            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: "Push" })],
        });
        if (!result.button.accept)
            return;
        // TODO: push assignment
    }
    async pullAssignment() {
        let result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
            title: "Pull Assignment",
            body: `Do you want to pull ${this.assignment.name}? This updates your assignment with the state of the server.`,
            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: "Pull" })],
        });
        if (!result.button.accept)
            return;
        // TODO: pull assignment
    }
    async releaseAssignment() {
        let result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
            title: "Release Assignment",
            body: `Do you want to release ${this.assignment.name} for all students? This can NOT be undone!`,
            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({ label: "Release" })],
        });
        if (!result.button.accept)
            return;
        result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
            title: "Confirmation",
            body: `Are you sure you want to release ${this.assignment.name}?`,
            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({ label: "Release" })],
        });
        if (!result.button.accept)
            return;
        // TODO: release assignment
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_2__.createElement("li", { key: this.index },
            react__WEBPACK_IMPORTED_MODULE_2__.createElement("div", { className: "assignment" },
                react__WEBPACK_IMPORTED_MODULE_2__.createElement("div", { className: "assignment-header" },
                    react__WEBPACK_IMPORTED_MODULE_2__.createElement("span", { onClick: this.toggleOpen },
                        react__WEBPACK_IMPORTED_MODULE_2__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__.Icon, { icon: "chevron-right", iconSize: this.iconSize, className: `collapse-icon-small ${this.state.isOpen ? "collapse-icon-small-open" : ""}` }),
                        react__WEBPACK_IMPORTED_MODULE_2__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__.Icon, { icon: "inbox", iconSize: this.iconSize, className: "flavor-icon" }),
                        this.assignment.name),
                    react__WEBPACK_IMPORTED_MODULE_2__.createElement("span", { className: "button-list" },
                        react__WEBPACK_IMPORTED_MODULE_2__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__.Button, { icon: 'edit', outlined: true, className: "assignment-button" }, "Edit"),
                        react__WEBPACK_IMPORTED_MODULE_2__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__.Button, { icon: 'search', outlined: true, className: "assignment-button", onClick: () => this.openPreview() }, "Preview"),
                        react__WEBPACK_IMPORTED_MODULE_2__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__.Button, { icon: 'git-push', intent: "success", outlined: true, className: "assignment-button", onClick: () => this.pushAssignment() }, "Push"),
                        react__WEBPACK_IMPORTED_MODULE_2__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__.Button, { icon: 'git-pull', intent: "primary", outlined: true, className: "assignment-button", onClick: () => this.pullAssignment() }, " Pull"),
                        react__WEBPACK_IMPORTED_MODULE_2__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__.Button, { icon: 'cloud-upload', outlined: true, className: "assignment-button", disabled: this.assignment.status == "created", onClick: () => this.releaseAssignment() }, "Release"),
                        react__WEBPACK_IMPORTED_MODULE_2__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__.Tag, { className: "assignment-tag", icon: "arrow-top-right", interactive: true, onClick: () => this.openGrading(this.lecture.id, this.assignment.id) },
                            this.state.submissions.length,
                            " ",
                            "Submission" + ((this.state.submissions.length > 1) ? "s" : "")))),
                react__WEBPACK_IMPORTED_MODULE_2__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__.Collapse, { isOpen: this.state.isOpen },
                    react__WEBPACK_IMPORTED_MODULE_2__.createElement("div", { className: "assignment-content" },
                        this.assignment.exercises.map((ex, i) => react__WEBPACK_IMPORTED_MODULE_2__.createElement("div", { className: "list-element", onClick: () => this.openFile(`${this.lectureName}/${this.assignment.name}/${ex.name}`) },
                            react__WEBPACK_IMPORTED_MODULE_2__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__.Icon, { icon: "edit", iconSize: this.iconSize, className: "flavor-icon" }),
                            ex.name)),
                        this.assignment.files.map((file, i) => react__WEBPACK_IMPORTED_MODULE_2__.createElement("div", { className: "list-element", onClick: () => this.openFile(`${this.lectureName}/${this.assignment.name}/${file.name}`) },
                            react__WEBPACK_IMPORTED_MODULE_2__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__.Icon, { icon: "document", iconSize: this.iconSize, className: "flavor-icon" }),
                            file.name)),
                        react__WEBPACK_IMPORTED_MODULE_2__.createElement("span", { className: "add-buttons" },
                            react__WEBPACK_IMPORTED_MODULE_2__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__.Button, { icon: "add", outlined: true, className: "assignment-button" }, "Add File"),
                            react__WEBPACK_IMPORTED_MODULE_2__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__.Button, { icon: "upload", outlined: true, className: "assignment-button" }, "Upload File"))))));
    }
}


/***/ }),

/***/ "./lib/components/grading/grading.js":
/*!*******************************************!*\
  !*** ./lib/components/grading/grading.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "GradingComponent": () => (/* binding */ GradingComponent)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _services_assignments_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../services/assignments.service */ "./lib/services/assignments.service.js");
/* harmony import */ var _services_lectures_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/lectures.service */ "./lib/services/lectures.service.js");
/* harmony import */ var _services_submissions_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/submissions.service */ "./lib/services/submissions.service.js");
/* harmony import */ var _material_ui_data_grid__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @material-ui/data-grid */ "webpack/sharing/consume/default/@material-ui/data-grid/@material-ui/data-grid");
/* harmony import */ var _material_ui_data_grid__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_material_ui_data_grid__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _blueprintjs_core_lib_cjs_components_button_buttons__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @blueprintjs/core/lib/cjs/components/button/buttons */ "./node_modules/@blueprintjs/core/lib/cjs/components/button/buttons.js");






class GradingComponent extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.state = {
            assignment: {},
            lecture: {},
            submissions: new Array(),
            isOpen: true,
            rows: new Array(),
        };
        this.lectureID = props.lectureID;
        this.assignmentID = props.assignmentID;
        this.title = props.title;
        this.columns = [
            { field: 'id', headerName: 'Id', width: 100 },
            { field: 'user', headerName: 'User', width: 130 },
            { field: 'date', headerName: 'Date', width: 200 },
            {
                field: '',
                headerName: '',
                width: 150,
                disableClickEventBubbling: true,
                disableColumnMenu: true,
                renderCell: (params) => (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_blueprintjs_core_lib_cjs_components_button_buttons__WEBPACK_IMPORTED_MODULE_2__.Button, { icon: "highlight", outlined: true }, "Autograde")),
            },
            { field: 'score', headerName: 'Score', width: 130 },
        ];
    }
    async componentDidMount() {
        let assignment = await (0,_services_assignments_service__WEBPACK_IMPORTED_MODULE_3__.fetchAssignment)(this.lectureID, this.assignmentID, false, true).toPromise();
        let lecture = await (0,_services_lectures_service__WEBPACK_IMPORTED_MODULE_4__.getLecture)(this.lectureID).toPromise();
        this.title.label = "Grading: " + assignment.name;
        this.setState({ assignment, lecture });
        (0,_services_submissions_service__WEBPACK_IMPORTED_MODULE_5__.getAllSubmissions)(lecture, assignment, false).subscribe(userSubmissions => {
            console.log(userSubmissions);
            this.setState(this.state.submissions = userSubmissions);
            //Temp rows for testing
            this.setState(this.state.rows = this.generateRows());
            console.log("rows:");
            console.log(this.state.rows);
        });
    }
    generateRows() {
        // let rows = [{ id: 10, user: "hasdf", date: "asdfadfa" }]
        let rows = new Array();
        //TODO: right now reading only the first 
        this.state.submissions.forEach(sub => { rows.push({ id: sub.user.id, user: sub.user.name, date: sub.submissions[0].submitted_at }); });
        return rows;
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { style: { height: "100%", display: "flex", flexDirection: "column" } },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_data_grid__WEBPACK_IMPORTED_MODULE_1__.DataGrid, { rows: this.state.rows, columns: this.columns, checkboxSelection: true, hideFooterPagination: true }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_blueprintjs_core_lib_cjs_components_button_buttons__WEBPACK_IMPORTED_MODULE_2__.Button, { icon: "highlight", color: "primary", outlined: true, style: { alignSelf: "flex-end", marginRight: "20px", marginBottom: "20px" } }, "Autograde selected")));
    }
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "GlobalObjects": () => (/* binding */ GlobalObjects),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _widgets_coursemanage__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./widgets/coursemanage */ "./lib/widgets/coursemanage.js");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _widgets_assignment_list__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./widgets/assignment-list */ "./lib/widgets/assignment-list.js");
/* harmony import */ var _widgets_grading__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./widgets/grading */ "./lib/widgets/grading.js");







// import { requestAPI } from './handler';
var AssignmentsCommandIDs;
(function (AssignmentsCommandIDs) {
    AssignmentsCommandIDs.create = 'assignments:create';
    AssignmentsCommandIDs.open = 'assignments:open';
})(AssignmentsCommandIDs || (AssignmentsCommandIDs = {}));
var CourseManageCommandIDs;
(function (CourseManageCommandIDs) {
    CourseManageCommandIDs.create = 'coursemanage:create';
    CourseManageCommandIDs.open = 'coursemanage:open';
})(CourseManageCommandIDs || (CourseManageCommandIDs = {}));
var GradingCommandIDs;
(function (GradingCommandIDs) {
    GradingCommandIDs.create = 'grading:create';
    GradingCommandIDs.open = 'grading:open';
})(GradingCommandIDs || (GradingCommandIDs = {}));
class GlobalObjects {
}
/**
 * Initialization data for the grading extension.
 */
const extension = {
    id: 'coursemanage:plugin',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__.ILauncher, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.INotebookTools],
    activate: (app, palette, launcher, nbtools) => {
        console.log('JupyterLab extension grading is activated!');
        console.log('JupyterFrontEnd:', app);
        console.log('ICommandPalette:', palette);
        GlobalObjects.commands = app.commands;
        /* ##### Course Manage View Widget ##### */
        let command = CourseManageCommandIDs.create;
        app.commands.addCommand(command, {
            execute: () => {
                // Create a blank content widget inside of a MainAreaWidget
                const gradingView = new _widgets_coursemanage__WEBPACK_IMPORTED_MODULE_4__.CourseManageView();
                const gradingWidget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget({ content: gradingView });
                gradingWidget.id = 'coursemanage-jupyterlab';
                gradingWidget.title.label = 'Course Management';
                gradingWidget.title.closable = true;
                return gradingWidget;
            }
        });
        command = CourseManageCommandIDs.open;
        app.commands.addCommand(command, {
            label: 'Course Management',
            execute: async () => {
                const gradingWidget = await app.commands.execute(CourseManageCommandIDs.create);
                if (!gradingWidget.isAttached) {
                    // Attach the widget to the main work area if it's not there
                    app.shell.add(gradingWidget, 'main');
                }
                // Activate the widget
                app.shell.activateById(gradingWidget.id);
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.checkIcon
        });
        // Add the command to the launcher
        console.log("Add course management launcher");
        launcher.add({
            command: command,
            category: 'Assignments',
            rank: 0
        });
        // Add the command to the palette.
        // palette.addItem({ command, category: 'Tutorial' });
        // Add the command to the Sidebar.
        // TODO: add grading to sidebar like file viewer and plugins etc
        /* ##### Assignment List Widget ##### */
        command = AssignmentsCommandIDs.create;
        app.commands.addCommand(command, {
            execute: () => {
                // Create a blank content widget inside of a MainAreaWidget
                const assignmentList = new _widgets_assignment_list__WEBPACK_IMPORTED_MODULE_5__.AssignmentList();
                const assignmentWidget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget({ content: assignmentList });
                assignmentWidget.id = 'assignments-jupyterlab';
                assignmentWidget.title.label = 'Assignments';
                assignmentWidget.title.closable = true;
                return assignmentWidget;
            }
        });
        command = AssignmentsCommandIDs.open;
        app.commands.addCommand(command, {
            label: 'Assignments',
            execute: async () => {
                const assignmentWidget = await app.commands.execute(AssignmentsCommandIDs.create);
                if (!assignmentWidget.isAttached) {
                    // Attach the widget to the main work area if it's not there
                    app.shell.add(assignmentWidget, 'main');
                }
                // Activate the widget
                app.shell.activateById(assignmentWidget.id);
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.editIcon
        });
        // Add the command to the launcher
        console.log("Add assignment launcher");
        launcher.add({
            command: command,
            category: 'Assignments',
            rank: 0
        });
        command = GradingCommandIDs.create;
        app.commands.addCommand(command, {
            execute: (args) => {
                const lectureID = typeof args['lectureID'] === 'undefined' ? null : args['lectureID'];
                const assignmentID = typeof args['assignmentID'] === 'undefined' ? null : args['assignmentID'];
                const gradingView = new _widgets_grading__WEBPACK_IMPORTED_MODULE_6__.GradingView({ lectureID, assignmentID });
                const gradingWidget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget({ content: gradingView });
                gradingWidget.id = 'grading-jupyterlab';
                gradingWidget.title.label = 'Grading';
                gradingWidget.title.closable = true;
                return gradingWidget;
            }
        });
        command = GradingCommandIDs.open;
        app.commands.addCommand(command, {
            label: 'Grading',
            execute: async (args) => {
                const gradingView = await app.commands.execute(GradingCommandIDs.create, args);
                if (!gradingView.isAttached) {
                    // Attach the widget to the main work area if it's not there
                    app.shell.add(gradingView, 'main');
                }
                // Activate the widget
                app.shell.activateById(gradingView.id);
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.editIcon
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ }),

/***/ "./lib/services/assignments.service.js":
/*!*********************************************!*\
  !*** ./lib/services/assignments.service.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "createAssignment": () => (/* binding */ createAssignment),
/* harmony export */   "getAllAssignments": () => (/* binding */ getAllAssignments),
/* harmony export */   "updateAssignment": () => (/* binding */ updateAssignment),
/* harmony export */   "fetchAssignment": () => (/* binding */ fetchAssignment),
/* harmony export */   "deleteAssignment": () => (/* binding */ deleteAssignment)
/* harmony export */ });
/* harmony import */ var _request_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./request.service */ "./lib/services/request.service.js");

function createAssignment(lectureId, assignment) {
    return (0,_request_service__WEBPACK_IMPORTED_MODULE_0__.request)(_request_service__WEBPACK_IMPORTED_MODULE_0__.HTTPMethod.POST, `/lectures/${lectureId}/assignments`, {}, assignment);
}
function getAllAssignments(lectureId) {
    return (0,_request_service__WEBPACK_IMPORTED_MODULE_0__.request)(_request_service__WEBPACK_IMPORTED_MODULE_0__.HTTPMethod.GET, `/lectures/${lectureId}/assignments`, {});
}
function updateAssignment(lectureId, assignment) {
    return (0,_request_service__WEBPACK_IMPORTED_MODULE_0__.request)(_request_service__WEBPACK_IMPORTED_MODULE_0__.HTTPMethod.PUT, `/lectures/${lectureId}/assignments/${assignment.id}`, {}, assignment);
}
function fetchAssignment(lectureId, assignmentId, instructor = false, metadataOnly = false) {
    let url = `/lectures/${lectureId}/assignments/${assignmentId}`;
    if (instructor || metadataOnly) {
        let searchParams = new URLSearchParams({
            "instructor-version": String(instructor),
            "metadata-only": String(metadataOnly)
        });
        url += '?' + searchParams;
    }
    return (0,_request_service__WEBPACK_IMPORTED_MODULE_0__.request)(_request_service__WEBPACK_IMPORTED_MODULE_0__.HTTPMethod.GET, url, {});
}
function deleteAssignment(lectureId, assignmentId) {
    (0,_request_service__WEBPACK_IMPORTED_MODULE_0__.request)(_request_service__WEBPACK_IMPORTED_MODULE_0__.HTTPMethod.DELETE, `/lectures/${lectureId}/assignments/${assignmentId}`, {});
}


/***/ }),

/***/ "./lib/services/lectures.service.js":
/*!******************************************!*\
  !*** ./lib/services/lectures.service.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "createLecture": () => (/* binding */ createLecture),
/* harmony export */   "getAllLectures": () => (/* binding */ getAllLectures),
/* harmony export */   "updateLecture": () => (/* binding */ updateLecture),
/* harmony export */   "getLecture": () => (/* binding */ getLecture),
/* harmony export */   "deleteLecture": () => (/* binding */ deleteLecture)
/* harmony export */ });
/* harmony import */ var _request_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./request.service */ "./lib/services/request.service.js");

function createLecture(lecture) {
    return (0,_request_service__WEBPACK_IMPORTED_MODULE_0__.request)(_request_service__WEBPACK_IMPORTED_MODULE_0__.HTTPMethod.POST, "/lectures", {}, lecture);
}
function getAllLectures() {
    return (0,_request_service__WEBPACK_IMPORTED_MODULE_0__.request)(_request_service__WEBPACK_IMPORTED_MODULE_0__.HTTPMethod.GET, "/lectures", {});
}
function updateLecture(lecture) {
    return (0,_request_service__WEBPACK_IMPORTED_MODULE_0__.request)(_request_service__WEBPACK_IMPORTED_MODULE_0__.HTTPMethod.PUT, `/lectures/${lecture.id}`, {}, lecture);
}
function getLecture(lectureId) {
    return (0,_request_service__WEBPACK_IMPORTED_MODULE_0__.request)(_request_service__WEBPACK_IMPORTED_MODULE_0__.HTTPMethod.GET, `/lectures/${lectureId}`, {});
}
function deleteLecture(lectureId) {
    (0,_request_service__WEBPACK_IMPORTED_MODULE_0__.request)(_request_service__WEBPACK_IMPORTED_MODULE_0__.HTTPMethod.DELETE, `/lectures/${lectureId}`, {});
}


/***/ }),

/***/ "./lib/services/request.service.js":
/*!*****************************************!*\
  !*** ./lib/services/request.service.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "HTTPMethod": () => (/* binding */ HTTPMethod),
/* harmony export */   "request": () => (/* binding */ request)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "webpack/sharing/consume/default/rxjs/rxjs");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(rxjs__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/internal/operators/switchMap.js");




var HTTPMethod;
(function (HTTPMethod) {
    HTTPMethod["GET"] = "GET";
    HTTPMethod["POST"] = "POST";
    HTTPMethod["PUT"] = "PUT";
    HTTPMethod["DELETE"] = "DELETE";
})(HTTPMethod || (HTTPMethod = {}));
function request(method, endPoint, options, body = null, url = "http://128.130.202.214:8000/services/mock") {
    options.method = method;
    if (body) {
        options.body = JSON.stringify(body);
    }
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    let requestUrl = "";
    if (url == null) {
        // ServerConnection only allows requests to notebook baseUrl
        requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, "/grader.grading_labextension", // API Namespace
        endPoint);
        console.log("Request " + method.toString() + " URL: " + requestUrl);
        return (0,rxjs__WEBPACK_IMPORTED_MODULE_2__.from)(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, options, settings)).pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_3__.switchMap)(async (response) => {
            let data = await response.text();
            if (data.length > 0) {
                try {
                    data = JSON.parse(data);
                }
                catch (error) {
                    console.log('Not a JSON response body.', response);
                }
            }
            return data;
        }));
    }
    else {
        requestUrl = url + endPoint;
        options.headers = {
            "Authorization": "Bearer 123"
        };
        console.log("Request " + method.toString() + " URL: " + requestUrl);
        return (0,rxjs__WEBPACK_IMPORTED_MODULE_2__.from)(fetch(requestUrl, options)).pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_3__.switchMap)(async (response) => {
            let data = await response.json();
            return data;
        }));
    }
}


/***/ }),

/***/ "./lib/services/submissions.service.js":
/*!*********************************************!*\
  !*** ./lib/services/submissions.service.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "submitAssignment": () => (/* binding */ submitAssignment),
/* harmony export */   "getSubmissions": () => (/* binding */ getSubmissions),
/* harmony export */   "getAllSubmissions": () => (/* binding */ getAllSubmissions),
/* harmony export */   "getFeedback": () => (/* binding */ getFeedback)
/* harmony export */ });
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/internal/operators/map.js");
/* harmony import */ var _request_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./request.service */ "./lib/services/request.service.js");


function submitAssignment(lecture, assignment) {
    return (0,_request_service__WEBPACK_IMPORTED_MODULE_0__.request)(_request_service__WEBPACK_IMPORTED_MODULE_0__.HTTPMethod.POST, `/lectures/${lecture.id}/assignments/${assignment.id}/submissions`, {}, {});
}
function getSubmissions(lecture, assignment, latest = false) {
    let url = `/lectures/${lecture.id}/assignments/${assignment.id}/submissions`;
    if (latest) {
        let searchParams = new URLSearchParams({
            "latest": String(latest)
        });
        url += '?' + searchParams;
    }
    return (0,_request_service__WEBPACK_IMPORTED_MODULE_0__.request)(_request_service__WEBPACK_IMPORTED_MODULE_0__.HTTPMethod.GET, url, {}).pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_1__.map)(array => array[0]));
}
function getAllSubmissions(lecture, assignment, latest = false, instructor = true) {
    let url = `/lectures/${lecture.id}/assignments/${assignment.id}/submissions`;
    if (latest || instructor) {
        let searchParams = new URLSearchParams({
            "instructor-version": String(instructor),
            "latest": String(latest)
        });
        url += '?' + searchParams;
    }
    return (0,_request_service__WEBPACK_IMPORTED_MODULE_0__.request)(_request_service__WEBPACK_IMPORTED_MODULE_0__.HTTPMethod.GET, url, {});
}
function getFeedback(lecture, assignment, latest = false, instructor = false) {
    let url = `/lectures/${lecture.id}/assignments/${assignment.id}/feedback`;
    if (latest || instructor) {
        let searchParams = new URLSearchParams({
            "instructor-version": String(instructor),
            "latest": String(latest)
        });
        url += '?' + searchParams;
    }
    return (0,_request_service__WEBPACK_IMPORTED_MODULE_0__.request)(_request_service__WEBPACK_IMPORTED_MODULE_0__.HTTPMethod.GET, url, {});
}


/***/ }),

/***/ "./lib/widgets/assignment-list.js":
/*!****************************************!*\
  !*** ./lib/widgets/assignment-list.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "AssignmentList": () => (/* binding */ AssignmentList)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_assignments_courses_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../components/assignments/courses.component */ "./lib/components/assignments/courses.component.js");



class AssignmentList extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    /*
     * Construct a new grading widget
     */
    constructor(options = {}) {
        super();
        this.id = options.id;
        this.addClass('AssignmentListWidget');
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_1__.createElement(_components_assignments_courses_component__WEBPACK_IMPORTED_MODULE_2__.CoursesComponent, null);
    }
}


/***/ }),

/***/ "./lib/widgets/coursemanage.js":
/*!*************************************!*\
  !*** ./lib/widgets/coursemanage.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CourseManageView": () => (/* binding */ CourseManageView)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_coursemanage_coursemanage_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../components/coursemanage/coursemanage.component */ "./lib/components/coursemanage/coursemanage.component.js");



class CourseManageView extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    /**
     * Construct a new grading widget
     */
    constructor(options = {}) {
        super();
        this.id = options.id;
        this.addClass('GradingWidget');
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_coursemanage_coursemanage_component__WEBPACK_IMPORTED_MODULE_2__.CourseManageComponent, null);
    }
}


/***/ }),

/***/ "./lib/widgets/grading.js":
/*!********************************!*\
  !*** ./lib/widgets/grading.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "GradingView": () => (/* binding */ GradingView)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_grading_grading__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../components/grading/grading */ "./lib/components/grading/grading.js");



class GradingView extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    /**
     * Construct a new grading widget
     */
    constructor(options) {
        super();
        this.lectureID = options.lectureID;
        this.assignmentID = options.assignmentID;
        this.addClass('GradingWidget');
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_grading_grading__WEBPACK_IMPORTED_MODULE_2__.GradingComponent, { lectureID: this.lectureID, assignmentID: this.assignmentID, title: this.title });
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js-webpack_sharing_consume_default_jupyterlab_statedb-webpack_sharing_consume_defau-d707a1.b4b8d0ec817a5ed1040a.js.map