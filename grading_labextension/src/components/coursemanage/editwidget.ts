import { Widget } from "@lumino/widgets";
import { Assignment } from "../../model/assignment";

export class EditForm extends Widget {
  /**
   * Create a edit form.
   */
  constructor(assignment : Assignment) {
    super({ node: Private.createNode(assignment) });
  }

  /**
   * Returns the input value.
   */
  getValue(): {name:string,date:string,type:string} {
      let obj = {name: "",date: "",type: ""};
      obj.name = this.node.querySelector("input").value;
      // TODO date reading not working
      const checkbox : HTMLInputElement = this.node.querySelector('input[type="checkbox"]');
      if(checkbox.checked) {
        obj.date = "";
      } else {
        const date : HTMLInputElement = this.node.querySelector('input[type="datetime-local"]');
        obj.date = date.value;

      }
      obj.type = this.node.querySelector("select").value;
      return obj;
  }
}


export function createEditForm(assignment : Assignment): EditForm {
  const form = new EditForm(assignment);
  return form;
}

/**
 * A namespace for private module data.
 */
namespace Private {

  export function createNode(assignment : Assignment): HTMLElement {
    const node = document.createElement('div');

    const namelabel = document.createElement('label');
    namelabel.textContent = "Assignment name:";
    const name = document.createElement('input');
    name.placeholder = assignment.name;

    const checklabel = document.createElement('label');
    checklabel.textContent = "No Deadline?";
    const checkboxdate = document.createElement('input');
    checkboxdate.type = 'checkbox';

    const date = document.createElement('input');
    date.classList.add('jp-mod-styled');
    date.type = 'datetime-local';    
    date.disabled = checkboxdate.checked;
    date.placeholder = assignment.due_date;

    const typelabel = document.createElement('label');
    typelabel.textContent = "Assignment type";
    const type = document.createElement('select');
    const useroption = document.createElement('option');
    useroption.textContent = 'user';
    useroption.selected = true;
    const groupoption = document.createElement('option');
    groupoption.textContent = 'group';

    namelabel.appendChild(name);
    node.appendChild(namelabel);

    checklabel.appendChild(checkboxdate);
    node.appendChild(checklabel);

    node.appendChild(date);

    type.appendChild(useroption);
    type.appendChild(groupoption);
    typelabel.appendChild(type);
    node.appendChild(typelabel);

    return node;
  }
}