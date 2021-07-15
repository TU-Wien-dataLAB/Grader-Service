// token: 0b79bab50daca910b000d4f1a2b675d604257e42

import { Lecture } from "../model/lecture";
import { HTTPMethod, request } from "./request.service";

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

  export async function loadPermissions(): Promise<void> {
    permissions = {};
    let response = await request<{ lecture_code: string, scope: number }[]>(HTTPMethod.GET, `/permissions`).toPromise();
    response.forEach(role => {
      permissions[role.lecture_code] = role.scope;
    });
  }

  export function getPermissions(): PermissionScopes {
    return permissions
  }

  export async function getScope(lecture: Lecture) {
    if (permissions == null) {
      return null;
    }
    return permissions[lecture.code];
  }
}