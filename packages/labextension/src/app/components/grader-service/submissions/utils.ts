import { Grading, SubmissionRow } from './submissions-data-table';
import { Submission } from '../../../../model/submission';

const toGrading = (_s: Submission): Grading => 'not_graded';

const toRow = (s: Submission, label?: string): SubmissionRow => ({
  id: String(s.id),
  student: s.user_display_name ?? '',
  label,
  score: s.score,
  grading: toGrading(s),
  feedback: s.feedback_status !== undefined, // TODO: real enum value
  submission: s
});

export const toSubmissionRows = (
  submissions: Array<Submission>
): Array<SubmissionRow> => {
  const byUser = new Map<number | undefined, Array<Submission>>();
  submissions.forEach(s => {
    byUser.set(s.user_id, [...(byUser.get(s.user_id) ?? []), s]);
  });

  return [...byUser.entries()].map(([userId, list]) => {
    if (list.length === 1) return toRow(list[0]);

    const sorted = [...list].sort((a, b) =>
      (a.submitted_at ?? '').localeCompare(b.submitted_at ?? '')
    );
    return {
      id: `user-${userId}`,
      student: sorted[0].user_display_name ?? '',
      subRows: sorted.map((s, i) => toRow(s, `Submission ${i + 1}`)).reverse()
    };
  });
};
