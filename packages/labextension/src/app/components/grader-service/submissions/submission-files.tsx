import React from 'react';
import { Submission } from '../../../../model/submission';
import { mockItems } from './table-mock-data';
import { SubmissionFile, SubmissionFolder } from './submission-details-dialog';
import { ManuallyGradedBadge } from '../../ui/badges';
import { BookIcon } from '../../../../assets/book-icon';

const formatScore = (score?: number, max = 200) =>
  score === undefined ? '' : `${score.toFixed(2)}/${max}`;

const ROW_GRID =
  'grid grid-cols-[minmax(0,15rem)_4rem_6rem_auto] items-center gap-x-6';

const FileLink = ({ name }: { name: string }) => (
  <a
    href="#"
    onClick={e => e.preventDefault()}
    title={name}
    className="flex min-w-0 items-center gap-2"
  >
    <BookIcon className="size-4 shrink-0" />
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
              className="ml-0.5 inline-block h-2.5 w-2.5 shrink-0 border-b-2 border-l-2 border-[#8D8D8D]"
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

type TProps = {
  files: Submission;
};

const SubmissionFiles = ({ files }: TProps) => {
  return (
    <div className="space-y-2">
      {mockItems.map(item =>
        item.kind === 'folder' ? (
          <FolderCard key={item.id} folder={item} />
        ) : (
          <FileRow key={item.id} file={item} />
        )
      )}
    </div>
  );
};

export default SubmissionFiles;
