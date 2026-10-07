import React, { useMemo, useState } from 'react';
import {
  CircleAlert,
  CircleCheck,
  Eye,
  History,
  TriangleAlert
} from 'lucide-react';
import type {
  ColumnFiltersState,
  OnChangeFn,
  RowSelectionState
} from '@tanstack/react-table';
import { Button } from '../../../shadcn-components/ui/button';
import {
  NestedTable,
  RowCheckbox,
  expanderColumn,
  selectColumn
} from '../../ui/nested-table/nested-table';
import type { DataTableColumnDef } from '../../ui/nested-table/nested-table';
import { Submission } from '../../../../model/submission';
import { SubmissionDetailsDialog } from './submission-details-dialog';
import { toSubmissionRows } from './utils';

/* row  */

export type Grading = 'graded' | 'failed' | 'not_graded';

export type SubmissionRow = {
  id: string;
  student: string;
  label?: string;
  score?: number;
  grading?: Grading;
  feedback?: boolean;
  submission?: Submission;
  subRows?: Array<SubmissionRow>;
};

const gradingLabel: Record<Grading, React.ReactNode> = {
  graded: (
    <span className="flex items-center gap-2">
      <CircleCheck color="#6A9816" className="size-4" /> Graded
    </span>
  ),
  failed: (
    <span className="flex items-center gap-2">
      <CircleAlert color="#DC182C" className="size-4" /> Grading failed
    </span>
  ),
  not_graded: (
    <span className="flex items-center gap-2">
      <TriangleAlert color="#C77700" className="size-4" /> Not graded
    </span>
  )
};

type ColumnHandlers = {
  onViewDetails: (row: SubmissionRow) => void;
  onViewLogs?: (row: SubmissionRow) => void;
};

const getColumns = ({
  onViewDetails,
  onViewLogs
}: ColumnHandlers): Array<DataTableColumnDef<SubmissionRow>> => [
  expanderColumn<SubmissionRow>(),
  selectColumn<SubmissionRow>(),
  {
    accessorKey: 'student',
    header: 'Name',
    cell: ({ row, getValue }) => (
      <div className={row.depth > 0 ? 'flex items-center gap-6' : ''}>
        {row.depth > 0 && <RowCheckbox row={row} />}
        <span className="truncate">
          {row.depth > 0 ? row.original.label : getValue<string>()}
        </span>
      </div>
    )
  },
  {
    accessorKey: 'score',
    header: 'Final score',
    enableGlobalFilter: false,
    cell: ({ getValue }) => {
      const score = getValue<number | undefined>();
      return score === undefined ? null : `${score.toFixed(2)} / 800`;
    }
  },
  {
    accessorKey: 'grading',
    header: 'Grading',
    enableGlobalFilter: false,
    filterFn: 'filterFn_equalsString',
    cell: ({ getValue }) => {
      const grading = getValue<Grading | undefined>();
      return grading ? gradingLabel[grading] : null;
    }
  },
  {
    accessorKey: 'feedback',
    header: 'Feedback',
    enableGlobalFilter: false,
    cell: ({ row, getValue }) => {
      if (row.original.grading === undefined) return null;
      return getValue<boolean>() ? (
        <span className="flex items-center gap-2">
          <CircleCheck color="#6A9816" className="size-4" /> Feedback given
        </span>
      ) : (
        <span className="flex items-center gap-2">
          <CircleAlert color="#DC182C" className="size-4" /> No feedback
        </span>
      );
    }
  },
  {
    id: 'actions',
    header: 'Actions',
    enableGlobalFilter: false,
    cell: ({ row }) =>
      row.original.submission === undefined ? null : (
        <div className="flex gap-1">
          <Button
            variant="ghost"
            size="icon"
            className="cursor-pointer"
            title="View submission details"
            aria-label="View submission details"
            onClick={() => onViewDetails(row.original)}
            ml-1
          >
            <Eye color="#006699" className="size-4" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            className="cursor-pointer"
            title="View logs"
            aria-label="View logs"
            onClick={() => onViewLogs?.(row.original)}
          >
            <History color="#006699" className="size-4" />
          </Button>
        </div>
      )
  }
];

// table

type TTableProps = {
  submissions: Array<Submission>;
  grading: string;
  search?: string;
  setSearch: (val: string) => void;
  rowSelection: RowSelectionState;
  onRowSelectionChange: OnChangeFn<RowSelectionState>;
  columnFilters: Set<string>;
};

const SubmissionsDataTable = ({
  submissions,
  grading,
  search,
  setSearch,
  rowSelection,
  onRowSelectionChange
}: TTableProps) => {
  const [selected, setSelected] = useState<Submission | null>(null);

  const data = useMemo(() => toSubmissionRows(submissions), [submissions]);

  const columns = useMemo(
    () =>
      getColumns({ onViewDetails: row => setSelected(row.submission ?? null) }),
    []
  );

  const columnFilters = useMemo<ColumnFiltersState>(
    () => (grading === 'all' ? [] : [{ id: 'grading', value: grading }]),
    [grading]
  );

  return (
    <div className="space-y-4 relative">
      <NestedTable
        columns={columns}
        data={data}
        getSubRows={row => row.subRows}
        getRowId={row => row.id}
        globalFilter={search}
        onGlobalFilterChange={setSearch}
        columnFilters={columnFilters}
        rowSelection={rowSelection}
        onRowSelectionChange={onRowSelectionChange}
        emptyMessage="No submissions match your filters."
      />

      <SubmissionDetailsDialog
        submission={selected}
        onClose={() => setSelected(null)}
      />
    </div>
  );
};

export default SubmissionsDataTable;
