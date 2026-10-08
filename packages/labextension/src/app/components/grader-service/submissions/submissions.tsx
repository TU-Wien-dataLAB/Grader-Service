import React, { useState } from 'react';
import NewSubmission from './new-submission';
import { SubmissionsView } from './submissions-view';

type TSubmissionsProps = {
  currentPath: string;
};

export type TSubmissionStates = 'view' | 'create-form' | 'edit-form';

const Submissions = ({ currentPath }: TSubmissionsProps) => {
  const [openNewSubmission, setOpenNewSubmission] = useState<boolean>(false);

  return (
    <div>
      {openNewSubmission ? (
        <NewSubmission
          currentPath={currentPath}
          setOpenNewSubmission={setOpenNewSubmission}
        />
      ) : (
        <SubmissionsView setOpenNewSubmission={setOpenNewSubmission} />
      )}
    </div>
  );
};

export default Submissions;
