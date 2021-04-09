import * as React from "react";
import { Submission } from "../../model/submission";

export interface SubmissionsListProps {
    submission: Submission;
    
}

export class SubmissionComponent extends React.Component {
    constructor(props: SubmissionsListProps) {
        super(props);
    }

    render() {
        return <div></div>
    }
}