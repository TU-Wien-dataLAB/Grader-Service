import * as React from 'react';
import { Assignment } from '../../model/assignment';
import { Lecture } from '../../model/lecture';
import { pullAssignment, resetAssignment } from '../../services/assignments.service';
import { getAllSubmissions, submitAssignment } from '../../services/submissions.service';
import { Button, Stack } from '@mui/material';
import { FilesList } from "../util/file-list";
import PublishRoundedIcon from "@mui/icons-material/PublishRounded";
import GetAppRoundedIcon from "@mui/icons-material/GetAppRounded";
import { SplitButton } from "../util/split-button";
import { AgreeDialog } from '../coursemanage/dialog';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import GradingIcon from '@mui/icons-material/Grading';
import { getFiles } from '../../services/file.service';
import { Submission } from '../../model/submission';


export interface IAssignmentFilesComponentProps {
    lecture: Lecture;
    assignment: Assignment;
    showAlert: (severity: string, msg: string) => void;
    setSubmissions: React.Dispatch<React.SetStateAction<Submission[]>>;
}

export const AssignmentFilesComponent = (props: IAssignmentFilesComponentProps) => {

    const [dialog, setDialog] = React.useState(false);
    const [path, setPath] = React.useState(`${props.lecture.code}/${props.assignment.name}`);
    const [hasFiles, setHasFiles] = React.useState(false);

    React.useEffect(() => {
        getFiles(path).then(files => setHasFiles(files.length > 0));
    }, [props]);

    const fetchAssignmentHandler = async (repo: "assignment" | "release" | "user") => {
        try {
            await pullAssignment(props.lecture.id, props.assignment.id, repo);
            props.showAlert('success', 'Successfully Pulled Repo');
        } catch (e) {
            props.showAlert('error', 'Error Fetching Assignment');
        }
    }

    const resetAssignmentHandler = async () => {
        try {
            await resetAssignment(props.lecture, props.assignment);
            props.showAlert('success', 'Successfully Reset Assignment');
        } catch (e) {
            props.showAlert('error', 'Error Reseting Assignment');
        }
        setDialog(false);
    }

    const submitAssignmentHandler = async () => {
        try {
            await submitAssignment(props.lecture, props.assignment);
            props.showAlert('success', 'Successfully Submitted Assignment');
        } catch (e) {
            props.showAlert('error', 'Error Submitting Assignment');
        }
        try {
            const submissions = await getAllSubmissions(props.lecture, props.assignment, false, false);
            props.setSubmissions(submissions)
        } catch (e) {
            props.showAlert('error', 'Error Updating Submissions');
        }
    }




    return (
        <div>
            <FilesList path={path} showAlert={props.showAlert} sx={{ m: 2, mt: 1 }} />
            <Stack direction={"row"} spacing={1} sx={{ m: 1, ml: 2 }}>
                <Button
                    variant='outlined'
                    size="small"
                >
                    <PublishRoundedIcon fontSize="small" sx={{ mr: 1 }} />
                    Push
                </Button>
                <Button
                    variant="outlined"
                    color="success"
                    size="small"
                    onClick={() => submitAssignmentHandler()}
                >
                    <GradingIcon fontSize="small" sx={{ mr: 1 }} />
                    Submit
                </Button>
                <SplitButton
                    variant="outlined"
                    size="small"
                    icon={<GetAppRoundedIcon fontSize="small" sx={{ mr: 1 }} />}
                    options={[
                        { name: "Pull User", onClick: () => fetchAssignmentHandler("user") },
                        { name: "Pull Release", onClick: () => fetchAssignmentHandler("release") }
                    ]}
                    selectedIndex={hasFiles ? 0 : 1}
                />
                <Button
                    variant="outlined"
                    size="small"
                    color="error"
                    onClick={() => setDialog(true)}
                >
                    <RestartAltIcon fontSize="small" sx={{ mr: 1 }} />
                    Reset
                </Button>
            </Stack>

            <AgreeDialog
                open={dialog}
                title={'Reset Assignment'}
                message={'This action will delete your current progress and reset the assignment! \n' +
                    'Therefore you should copy and paste your work to a different directory before progressing. '}
                handleAgree={resetAssignmentHandler}
                handleDisagree={() => setDialog(false)} />
        </div>
    );
}