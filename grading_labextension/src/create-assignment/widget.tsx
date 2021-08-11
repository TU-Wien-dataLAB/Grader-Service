/* eslint-disable @typescript-eslint/no-empty-function */
import { ReactWidget } from '@jupyterlab/apputils';

import { Cell, CodeCell, MarkdownCell } from '@jupyterlab/cells';

import { runIcon, stopIcon, LabIcon } from '@jupyterlab/ui-components';

import { ISessionContext } from '@jupyterlab/apputils';

import React, { useEffect, useState } from 'react';

/**
 * PlayButton
 *
 * Note: A react component rendering a simple button with a jupyterlab icon
 *
 * @param icon - The subclass of LabIcon to show.
 * @param onClick - Method to call when the button is clicked.
 */
interface IPlayButtonComponent {
  icon: LabIcon;
  onClick: () => void;
}

const PlayButton = ({ icon, onClick }: IPlayButtonComponent) => (
  <button type="button" onClick={() => onClick()} className="cellPlayButton">
    <LabIcon.resolveReact
      icon={icon}
      className="cellPlayButton-icon"
      tag="span"
      width="15px"
      height="15px"
    />
  </button>
);

/**
 * makeCancelable
 *
 * Note: Permits a Promise to be cancelled rather than to execute a
 * chained .then callback which is necessary if the component
 * has been unmounted
 *
 * Lifted from the long running discussion here:
 * https://github.com/facebook/react/issues/5465#issuecomment-157888325
 *
 * @param promise - The Promise to make cancellable.
 */
function makeCancelable<T>(promise: Promise<T>) {
  let active = true;
  return {
    cancel() {
      active = false;
    },
    promise: promise.then(
      value => (active ? value : new Promise(() => {})),
      reason => (active ? reason : new Promise(() => {}))
    )
  };
}

/**
 * CodeCellPlayButtonComponent
 *
 * Note: handles executing and rendering a Play button for
 * a given code cell. Attempts to show whether the cell is
 * running or not via the stop and start icons respectively.
 * If the cell is deemed to be running, the button instead
 * interrupts the kernel when pressed.
 *
 * @param cell - The CodeCell parent.
 * @param session - The current kernel session object
 */
interface ICodeCellPlayButtonComponent {
  cell: CodeCell;
  session: ISessionContext;
}

const CodeCellPlayButtonComponent = ({
  cell,
  session
}: ICodeCellPlayButtonComponent): JSX.Element => {
  // A hacky way to find out if we're currently running
  // anything, but doesn't matter greatly because the status
  // will soon be updated by the returned kernel future promise
  const [isRunning, setIsRunning] = useState(
    !!(cell.promptNode.textContent === '[*]:')
  );

  const executeCell = async () => {
    CodeCell.execute(cell, session);
    setIsRunning(true);
  };

  const interruptKernel = () => {
    void session.session?.kernel?.interrupt();
  };

  useEffect(() => {
    const codeCellFuture = cell.outputArea.future;
    if (!codeCellFuture) {
      return;
    }
    const { promise, cancel } = makeCancelable(codeCellFuture.done);
    promise.then(() => {
      setIsRunning(false);
    });
    return () => {
      cancel();
    };
  }, [isRunning]);

  return (
    <PlayButton
      icon={isRunning ? stopIcon : runIcon}
      onClick={() => (isRunning ? interruptKernel : executeCell)()}
    />
  );
};

/**
 * MarkdownCellPlayButtonComponent
 *
 * Note: Renders the cell's markdown when pressed
 *
 * @param cell - The MarkdownCell parent.
 */
interface IMarkdownPlayButtonComponent {
  cell: MarkdownCell;
}

const MarkdownCellPlayButtonComponent = ({
  cell
}: IMarkdownPlayButtonComponent) => {
  const executeCell = () => {
    cell.rendered = true;
  };

  return <PlayButton icon={runIcon} onClick={() => executeCell()} />;
};

export class CellPlayButton extends ReactWidget {
  /**
   * Constructs a new CellPlayButton widget.
   *
   * Note: Depending on the type of cell encountered
   * tries to render an appropriate play button
   * component.
   */
  cell: Cell = null;
  session: ISessionContext = null;

  constructor(cell: Cell, session: ISessionContext) {
    super();
    this.cell = cell;
    this.session = session;
    this.addClass('jp-CellPlayButton');
  }

  render(): JSX.Element {
    switch (this.cell.model.type) {
      case 'markdown':
        return (
          <MarkdownCellPlayButtonComponent cell={this.cell as MarkdownCell} />
        );
      case 'code':
        return (
          <CodeCellPlayButtonComponent
            cell={this.cell as CodeCell}
            session={this.session}
          />
        );
      default:
        break;
    }
  }
}
