import * as React from "react";
import { Submission } from "../../model/submission";
import { Table } from "@blueprintjs/table";

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