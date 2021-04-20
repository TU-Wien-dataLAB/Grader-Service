(self["webpackChunkgrading"] = self["webpackChunkgrading"] || []).push([["style_index_js"],{

/***/ "./node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \**************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_components_assignment_list_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! -!../node_modules/css-loader/dist/cjs.js!./components/assignment-list.css */ "./node_modules/css-loader/dist/cjs.js!./style/components/assignment-list.css");
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_components_assignment_css__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! -!../node_modules/css-loader/dist/cjs.js!./components/assignment.css */ "./node_modules/css-loader/dist/cjs.js!./style/components/assignment.css");
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_components_courses_css__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! -!../node_modules/css-loader/dist/cjs.js!./components/courses.css */ "./node_modules/css-loader/dist/cjs.js!./style/components/courses.css");
// Imports





var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_components_assignment_list_css__WEBPACK_IMPORTED_MODULE_2__.default);
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_components_assignment_css__WEBPACK_IMPORTED_MODULE_3__.default);
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_components_courses_css__WEBPACK_IMPORTED_MODULE_4__.default);
// Module
___CSS_LOADER_EXPORT___.push([module.id, ":root {\n  --text-color: #2e373d;\n  --accent-color: rgb(243, 114, 0);\n  --submit-color: #0d8050;\n}", "",{"version":3,"sources":["webpack://./style/base.css"],"names":[],"mappings":"AAIA;EACE,qBAAqB;EACrB,gCAAgC;EAChC,uBAAuB;AACzB","sourcesContent":["@import url('components/assignment-list.css');\n@import url('components/assignment.css');\n@import url('components/courses.css');\n\n:root {\n  --text-color: #2e373d;\n  --accent-color: rgb(243, 114, 0);\n  --submit-color: #0d8050;\n}"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/components/assignment-list.css":
/*!************************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/components/assignment-list.css ***!
  \************************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, ".AssignmentComponent {\n  color: var(--text-color);\n}\n\n.collapse-header {\n  color: var(--text-color);\n  font-size: 12pt;\n  margin: 8pt;\n  padding-left: 10pt;\n  padding-top: 6pt;\n  user-select: none;\n  -webkit-user-select: none;\n  cursor: pointer;\n\n  /* border-top: 1px solid var(--text-color); */\n}\n\n.collapse-header:hover .flavor-icon {\n  color: var(--accent-color);\n}\n\n.collapse-body {\n  margin-left: 10pt;\n}\n\n.collapse-body ul {\n  list-style-type: none;\n}\n\n.collapse-icon {\n  float: right;\n  color: var(--text-color);\n  transition: transform .2s cubic-bezier(.4,1,.75,.9), -webkit-transform .2s cubic-bezier(.4,1,.75,.9);\n}\n\n.collapse-icon-open {\n  -webkit-transform: rotate(180deg);\n  transform: rotate(180deg);\n}\n\n.flavor-icon {\n  color: var(--text-color);\n  padding-right: 6pt;\n  transition: 0.2s;\n}", "",{"version":3,"sources":["webpack://./style/components/assignment-list.css"],"names":[],"mappings":"AAAA;EACE,wBAAwB;AAC1B;;AAEA;EACE,wBAAwB;EACxB,eAAe;EACf,WAAW;EACX,kBAAkB;EAClB,gBAAgB;EAChB,iBAAiB;EACjB,yBAAyB;EACzB,eAAe;;EAEf,6CAA6C;AAC/C;;AAEA;EACE,0BAA0B;AAC5B;;AAEA;EACE,iBAAiB;AACnB;;AAEA;EACE,qBAAqB;AACvB;;AAEA;EACE,YAAY;EACZ,wBAAwB;EACxB,oGAAoG;AACtG;;AAEA;EACE,iCAAiC;EACjC,yBAAyB;AAC3B;;AAEA;EACE,wBAAwB;EACxB,kBAAkB;EAClB,gBAAgB;AAClB","sourcesContent":[".AssignmentComponent {\n  color: var(--text-color);\n}\n\n.collapse-header {\n  color: var(--text-color);\n  font-size: 12pt;\n  margin: 8pt;\n  padding-left: 10pt;\n  padding-top: 6pt;\n  user-select: none;\n  -webkit-user-select: none;\n  cursor: pointer;\n\n  /* border-top: 1px solid var(--text-color); */\n}\n\n.collapse-header:hover .flavor-icon {\n  color: var(--accent-color);\n}\n\n.collapse-body {\n  margin-left: 10pt;\n}\n\n.collapse-body ul {\n  list-style-type: none;\n}\n\n.collapse-icon {\n  float: right;\n  color: var(--text-color);\n  transition: transform .2s cubic-bezier(.4,1,.75,.9), -webkit-transform .2s cubic-bezier(.4,1,.75,.9);\n}\n\n.collapse-icon-open {\n  -webkit-transform: rotate(180deg);\n  transform: rotate(180deg);\n}\n\n.flavor-icon {\n  color: var(--text-color);\n  padding-right: 6pt;\n  transition: 0.2s;\n}"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/components/assignment.css":
/*!*******************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/components/assignment.css ***!
  \*******************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, "\n.assignment-header {\n  margin-top: 12pt;\n  margin-bottom: 8pt;\n  margin-right: 16pt;\n  user-select: none;\n  -webkit-user-select: none;\n  cursor: pointer;\n}\n\n.assignment-title,\n.assignment-content,\n.assignment-create {\n  margin-left: 10pt;\n}\n\n.assignment-content {\n  padding-bottom: 10pt;\n}\n\n.assignment-header:hover .flavor-icon {\n  color: var(--accent-color);\n}\n\n.assignment-header:first-child {\n  margin-top: -5pt;\n}\n\n.assignment-title {\n  margin-bottom: 5pt;\n  user-select: none;\n  -webkit-user-select: none;\n}\n\n.assignment-title:first-child {\n  margin-top: -5pt;\n}\n\n.assignment-title:hover .flavor-icon {\n  color: var(--accent-color);\n}\n\n.list-element, .submission-element  {\n  margin-left: 16pt;\n  padding-top: 3pt;\n  cursor: pointer;\n}\n\n.list-element:hover {\n  color: var(--accent-color);\n  text-decoration: underline; \n}\n\n.list-element:hover .flavor-icon {\n  color: var(--accent-color);\n}\n\n\n.collapse-icon-small {\n  color: var(--text-color);\n  transition: transform .2s cubic-bezier(.4,1,.75,.9), -webkit-transform .2s cubic-bezier(.4,1,.75,.9);\n}\n\n.collapse-icon-small-open {\n  -webkit-transform: rotate(90deg);\n  transform: rotate(90deg);\n}\n\n.button-list {\n  margin-left: 10%;\n}\n.add-buttons {\n  margin-top: 4pt;\n}\n\n.assignment-button,\n.assignment-tag {\n  min-height: 18px;\n  margin-right: 4pt;\n  padding: 2pt;\n}\n\n.assignment-button span,\n.assignment-tag span {\n  font-size: 9pt;\n}\n\n.assignment-button span svg,\n.assignment-tag span svg  {\n  width: 9pt;\n  height: 9pt;\n}\n", "",{"version":3,"sources":["webpack://./style/components/assignment.css"],"names":[],"mappings":";AACA;EACE,gBAAgB;EAChB,kBAAkB;EAClB,kBAAkB;EAClB,iBAAiB;EACjB,yBAAyB;EACzB,eAAe;AACjB;;AAEA;;;EAGE,iBAAiB;AACnB;;AAEA;EACE,oBAAoB;AACtB;;AAEA;EACE,0BAA0B;AAC5B;;AAEA;EACE,gBAAgB;AAClB;;AAEA;EACE,kBAAkB;EAClB,iBAAiB;EACjB,yBAAyB;AAC3B;;AAEA;EACE,gBAAgB;AAClB;;AAEA;EACE,0BAA0B;AAC5B;;AAEA;EACE,iBAAiB;EACjB,gBAAgB;EAChB,eAAe;AACjB;;AAEA;EACE,0BAA0B;EAC1B,0BAA0B;AAC5B;;AAEA;EACE,0BAA0B;AAC5B;;;AAGA;EACE,wBAAwB;EACxB,oGAAoG;AACtG;;AAEA;EACE,gCAAgC;EAChC,wBAAwB;AAC1B;;AAEA;EACE,gBAAgB;AAClB;AACA;EACE,eAAe;AACjB;;AAEA;;EAEE,gBAAgB;EAChB,iBAAiB;EACjB,YAAY;AACd;;AAEA;;EAEE,cAAc;AAChB;;AAEA;;EAEE,UAAU;EACV,WAAW;AACb","sourcesContent":["\n.assignment-header {\n  margin-top: 12pt;\n  margin-bottom: 8pt;\n  margin-right: 16pt;\n  user-select: none;\n  -webkit-user-select: none;\n  cursor: pointer;\n}\n\n.assignment-title,\n.assignment-content,\n.assignment-create {\n  margin-left: 10pt;\n}\n\n.assignment-content {\n  padding-bottom: 10pt;\n}\n\n.assignment-header:hover .flavor-icon {\n  color: var(--accent-color);\n}\n\n.assignment-header:first-child {\n  margin-top: -5pt;\n}\n\n.assignment-title {\n  margin-bottom: 5pt;\n  user-select: none;\n  -webkit-user-select: none;\n}\n\n.assignment-title:first-child {\n  margin-top: -5pt;\n}\n\n.assignment-title:hover .flavor-icon {\n  color: var(--accent-color);\n}\n\n.list-element, .submission-element  {\n  margin-left: 16pt;\n  padding-top: 3pt;\n  cursor: pointer;\n}\n\n.list-element:hover {\n  color: var(--accent-color);\n  text-decoration: underline; \n}\n\n.list-element:hover .flavor-icon {\n  color: var(--accent-color);\n}\n\n\n.collapse-icon-small {\n  color: var(--text-color);\n  transition: transform .2s cubic-bezier(.4,1,.75,.9), -webkit-transform .2s cubic-bezier(.4,1,.75,.9);\n}\n\n.collapse-icon-small-open {\n  -webkit-transform: rotate(90deg);\n  transform: rotate(90deg);\n}\n\n.button-list {\n  margin-left: 10%;\n}\n.add-buttons {\n  margin-top: 4pt;\n}\n\n.assignment-button,\n.assignment-tag {\n  min-height: 18px;\n  margin-right: 4pt;\n  padding: 2pt;\n}\n\n.assignment-button span,\n.assignment-tag span {\n  font-size: 9pt;\n}\n\n.assignment-button span svg,\n.assignment-tag span svg  {\n  width: 9pt;\n  height: 9pt;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/components/courses.css":
/*!****************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/components/courses.css ***!
  \****************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, ".course-list {\n  overflow: scroll;\n  height: 100%;\n}", "",{"version":3,"sources":["webpack://./style/components/courses.css"],"names":[],"mappings":"AAAA;EACE,gBAAgB;EAChB,YAAY;AACd","sourcesContent":[".course-list {\n  overflow: scroll;\n  height: 100%;\n}"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./style/base.css":
/*!************************!*\
  !*** ./style/base.css ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./base.css */ "./node_modules/css-loader/dist/cjs.js!./style/base.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_1__.default, options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_1__.default.locals || {});

/***/ }),

/***/ "./style/index.js":
/*!************************!*\
  !*** ./style/index.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./base.css */ "./style/base.css");



/***/ })

}]);
//# sourceMappingURL=style_index_js.999da25b1e4e3481833e.js.map