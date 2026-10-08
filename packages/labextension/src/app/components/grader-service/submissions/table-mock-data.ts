import { Submission } from '../../../../model/submission';
import { AutoStatus } from '../../../../model/autoStatus';
import { FeedbackStatus } from '../../../../model/feedbackStatus';
import { ManualStatus } from '../../../../model/manualStatus';
import { SubmissionFile, SubmissionFolder } from './submission-details-dialog';

const status = <T>(value: string) => value as unknown as T;

export const mockSubmissionsData: Array<Submission> = [
  {
    id: 1,
    assignid: 10,
    user_id: 1,
    user_display_name: 'Lina Hoffmann',
    submitted_at: '2025-11-10T21:30:00Z',
    auto_status: status<AutoStatus>('graded'),
    feedback_status: status<FeedbackStatus>('given'),
    grading_score: 750,
    score: 750,
    commit_hash: 'a1b2c3d'
  },
  {
    id: 2,
    assignid: 10,
    user_id: 1,
    user_display_name: 'Lina Hoffmann',
    submitted_at: '2025-11-11T22:59:00Z',
    auto_status: status<AutoStatus>('failed'),
    grading_score: 279,
    score: 283, // 279 + 4 extra credit
    commit_hash: 'e4f5a6b'
  },
  {
    id: 3,
    assignid: 10,
    user_id: 2,
    user_display_name: 'Mateo Alvarez',
    submitted_at: '2025-11-11T20:10:00Z',
    auto_status: status<AutoStatus>('not_graded'),
    grading_score: 0,
    score: 0
  },
  {
    id: 4,
    assignid: 10,
    user_id: 3,
    user_display_name: 'Aisha Rahman',
    submitted_at: '2025-11-09T18:45:00Z',
    auto_status: status<AutoStatus>('graded'),
    manual_status: status<ManualStatus>('graded'),
    feedback_status: status<FeedbackStatus>('given'),
    grading_score: 800,
    score: 800,
    edited: true
  }
];

export const mockSubmission: Submission = {
  id: 1,
  assignid: 10,
  user_id: 1,
  user_display_name: 'Lina Hoffmann',
  submitted_at: '2025-11-10T21:30:00Z',
  auto_status: status<AutoStatus>('graded'),
  feedback_status: status<FeedbackStatus>('given'),
  grading_score: 750,
  score: 750,
  commit_hash: 'a1b2c3d'
};

export type SubmissionItem =
  ({ kind: 'file' } & SubmissionFile) | ({ kind: 'folder' } & SubmissionFolder);

export const mockItems: Array<SubmissionItem> = [
  {
    kind: 'file',
    id: 'f1',
    name: 'Notebook1_Abgabe_Hoffmann_Lina.ipynb',
    score: 92.5,
    manuallyGraded: true
  },
  {
    kind: 'file',
    id: 'f2',
    name: 'Notebook2_Abgabe_Hoffmann_Lina.ipynb',
    score: 92.5
  },
  {
    kind: 'folder',
    id: 'd1',
    name: 'Folder1_Abgabe_Hoffmann_Lina',
    files: [
      { id: 'd1a', name: 'Name' },
      { id: 'd1b', name: 'Name', score: 92.5 },
      { id: 'd1c', name: 'Name' }
    ]
  },
  {
    kind: 'file',
    id: 'f4',
    name: 'Notebook4_Abgabe_Hoffmann_Lina.ipynb',
    score: 0
  }
];
