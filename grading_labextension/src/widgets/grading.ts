import { Widget } from '@lumino/widgets';

export class GradingView extends Widget {
  /**
   * Construct a new grading widget
   */
     constructor(options: GradingView.IOptions = {}) {
       super();
      this.id = options.id
     }

}

export namespace GradingView {
  /**
   * An options object for initializing a grading view widget.
   */
  export interface IOptions {
    /**
     * The widget/DOM id of the grading view.
     */
    id?: string;
  }
}