import React from 'react';
import { Button } from '../../../shadcn-components/ui/button';
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle
} from '../../../shadcn-components/ui/sheet';
import { Submission } from '../../../../model/submission';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from '../../../shadcn-components/ui/select';
import { BookOpen } from 'lucide-react';
import { mockItems } from './table-mock-data';
import { Separator } from '../../../shadcn-components/ui/separator';
import {
  AutomaticallyGradedBadge,
  EditedBadge,
  ManuallyGradedBadge
} from '../../ui/badges';
import { EmptyState } from '../../utils/empty-state';
import { EmptyIcon } from '../../../../assets/empty-icon';

type SubmissionDetailsDialogProps = {
  submission: Submission | null;
  onClose: () => void;
};

export type SubmissionFile = {
  id: string;
  name: string;
  score?: number;
  maxScore?: number;
  manuallyGraded?: boolean;
};

export type SubmissionFolder = {
  id: string;
  name: string;
  files: Array<SubmissionFile>;
};

const getGradingMethod = (s: Submission): 'automatic' | 'manual' =>
  s.manual_status !== undefined ? 'manual' : 'automatic';

const hasFeedback = (s: Submission): boolean => s.feedback_status !== undefined;

const pad = (n: number) => String(n).padStart(2, '0');

const formatSubmittedAt = (iso?: string) => {
  if (!iso) return '—';
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return `${pad(d.getDate())}.${pad(d.getMonth() + 1)}.${d.getFullYear()} ${pad(
    d.getHours()
  )}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
};

const formatScore = (score?: number, max = 200) =>
  score === undefined ? '' : `${score.toFixed(2)}/${max}`;

const DetailRow = ({
  label,
  children
}: {
  label: string;
  children: React.ReactNode;
}) => (
  <div className="flex leading-[20px]">
    <dt className="font-medium text-sm text-foreground flex-1">{label}</dt>
    <dd className="flex-3 text-sm">{children}</dd>
  </div>
);

const ROW_GRID =
  'grid grid-cols-[minmax(0,15rem)_4rem_6rem_auto] items-center gap-x-6';

const FileLink = ({ name }: { name: string }) => (
  <a
    href="#"
    onClick={e => e.preventDefault()}
    title={name}
    className="flex min-w-0 items-center gap-2"
  >
    <BookOpen color="#006699" className="size-4 shrink-0" />
    <span className="truncate text-sm text-[#006699] underline underline-offset-2">
      {name}
    </span>
  </a>
);

const FileRow = ({ file }: { file: SubmissionFile }) => (
  <div className={`${ROW_GRID} rounded-xs bg-white py-2 px-4`}>
    <FileLink name={file.name} />

    <span className="text-sm">{formatScore(file.score, file.maxScore)}</span>
    <span>{file.manuallyGraded && <ManuallyGradedBadge />}</span>
  </div>
);

const FolderCard = ({ folder }: { folder: SubmissionFolder }) => (
  <div className="rounded-xs bg-white py-2 px-4">
    <p className="font-medium">{folder.name}</p>
    <ul className="mt-3 space-y-3">
      {folder.files.map(file => (
        <li key={file.id} className={ROW_GRID}>
          <div className="flex min-w-0 items-center gap-3">
            <span
              aria-hidden="true"
              className="ml-0.5 inline-block h-2.5 w-3 shrink-0 border-b-2 border-l-2 border-[#8D8D8D]"
            />
            <FileLink name={file.name} />
          </div>
          <span className="text-sm">
            {formatScore(file.score, file.maxScore)}
          </span>
          <span />
        </li>
      ))}
    </ul>
  </div>
);

export const SubmissionDetailsDialog = ({
  submission,
  onClose
}: SubmissionDetailsDialogProps) => (
  <Sheet open={submission !== null} onOpenChange={open => !open && onClose()}>
    <SheetContent
      side="right"
      className="gap-0 overflow-y-auto bg-[#F5F5F5] pb-6 absolute"
      style={{ width: '100%', maxWidth: '100%' }}
    >
      {submission && (
        <>
          <SheetHeader className="px-6 py-6">
            <SheetTitle className="text-2xl font-bold flex gap-4">
              <h3>Submission details</h3>
              <EditedBadge />
            </SheetTitle>
          </SheetHeader>
          <Separator />

          <div className="px-6 text-base">
            {/* Details */}
            <section className="py-6">
              <h3 className="text-xl font-bold mb-2">Details</h3>
              <dl className="flex flex-col flex-start gap-3">
                <DetailRow label="Assignment">Submission details</DetailRow>
                <DetailRow label="Name">
                  {submission.user_display_name ?? '—'}
                </DetailRow>
                <DetailRow label="Grading method">
                  {getGradingMethod(submission) === 'automatic' ? (
                    <AutomaticallyGradedBadge />
                  ) : (
                    <ManuallyGradedBadge />
                  )}
                </DetailRow>
                <DetailRow label="Feedback">
                  {hasFeedback(submission) ? 'Feedback given' : 'No Feedback'}
                </DetailRow>
                <DetailRow label="Submitted at">
                  {formatSubmittedAt(submission.submitted_at)}
                </DetailRow>
                <DetailRow label="Achieved points">
                  {(submission.grading_score ?? 0).toFixed(2)}/5
                </DetailRow>
                <DetailRow label="Extra credit">
                  {Math.max(
                    0,
                    (submission.score ?? 0) - (submission.grading_score ?? 0)
                  ).toFixed(2)}
                </DetailRow>
                <DetailRow label="Final score">
                  {submission.score ?? '—'}
                </DetailRow>
                <DetailRow label="Score scaling">
                  <Select
                    value={
                      submission.score_scaling !== undefined
                        ? String(submission.score_scaling)
                        : undefined
                    }
                  >
                    <SelectTrigger className="w-64 rounded-none border-[#b5b5b5] bg-white">
                      <SelectValue placeholder="Choose option" />
                    </SelectTrigger>
                    <SelectContent>
                      {Array(4).map(option => (
                        <SelectItem
                          key={option.value}
                          value={String(option.value)}
                        >
                          {option.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </DetailRow>
              </dl>
            </section>

            <section className="py-6">
              <div className="flex justify-between mb-2">
                <h3 className="text-xl font-bold mb-2">Submission</h3>
                <Button variant="outline">Autograde</Button>
              </div>

              {mockItems && mockItems.length > 0 ? (
                <>
                  <div className="space-y-2">
                    {mockItems.map(item =>
                      item.kind === 'folder' ? (
                        <FolderCard key={item.id} folder={item} />
                      ) : (
                        <FileRow key={item.id} file={item} />
                      )
                    )}
                  </div>
                  <div className="flex flex-start gap-4 mt-4">
                    <Button variant="default">Generate feedback</Button>
                    <Button variant="outline">Edit submission</Button>
                  </div>
                </>
              ) : (
                <div className="mt-10 flex flex-col items-center">
                  <EmptyState
                    title={'No entries found'}
                    icon={<EmptyIcon />}
                    description={
                      'Start editing to load the submission and make changes.'
                    }
                  />
                  <Button className="w-fit" variant="default">
                    Start editing
                  </Button>
                </div>
              )}
            </section>
          </div>
        </>
      )}
    </SheetContent>
  </Sheet>
);
