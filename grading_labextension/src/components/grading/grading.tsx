/* eslint-disable no-useless-escape */
/* eslint-disable eqeqeq */
/* eslint-disable prefer-const */
/* eslint-disable no-constant-condition */
/* eslint-disable @typescript-eslint/no-array-constructor */
import { Title, Widget } from '@lumino/widgets';
import * as React from 'react';
import { Assignment } from '../../model/assignment';
import { Lecture } from '../../model/lecture';
import { Submission } from '../../model/submission';
import { fetchAssignment } from '../../services/assignments.service';
import { getLecture } from '../../services/lectures.service';
import { getAllSubmissions } from '../../services/submissions.service';

import {
  DataGrid,
  GridApi,
  GridCellParams,
  GridCellValue,
  GridColDef
} from '@material-ui/data-grid';
import { Button } from '@blueprintjs/core/lib/cjs/components/button/buttons';
import { ItemRenderer, Select } from '@blueprintjs/select';
import { User } from '../../model/user';
import { MenuItem } from '@blueprintjs/core';

export interface IGradingProps {
  lectureID: number;
  assignmentID: number;
  title: Title<Widget>;
}

const StringSelect = Select.ofType<string>();

export class GradingComponent extends React.Component<IGradingProps> {
  public lectureID: number;
  public assignmentID: number;
  public title: Title<Widget>;

  public submissions: Submission[];
  public lectureId: number;
  public assignmentId: number;
  public columns: GridColDef[];
  public state = {
    assignment: {},
    lecture: {},
    submissions: new Array<{ user: User; submissions: Submission[] }>(),
    option: 'latest',
    rows: new Array(),
    selected: new Array()
  };

  constructor(props: IGradingProps) {
    super(props);
    this.lectureID = props.lectureID;
    this.assignmentID = props.assignmentID;
    this.title = props.title;
    this.columns = [
      { field: 'id', headerName: 'Id', width: 110 },
      { field: 'name', headerName: 'User', width: 130 },
      { field: 'date', headerName: 'Date', width: 250 },
      { field: 'status', headerName: 'Status', width: 250 },
      {
        field: 'Autograde',
        headerName: '',
        sortable: false,
        width: 150,
        disableClickEventBubbling: true,
        renderCell: params => {
          const onClick = () => {
            const api: GridApi = params.api;
            const fields = api
              .getAllColumns()
              .map(c => c.field)
              .filter(c => c !== '__check__' && !!c);
            const thisRow: Record<string, GridCellValue> = {};

            fields.forEach(f => {
              thisRow[f] = params.getValue(params.id, f);
            });

            return alert(JSON.stringify(thisRow, null, 4));
          };

          return (
            <Button icon="highlight" onClick={onClick} outlined>
              Autograde
            </Button>
          );
        }
      } as GridColDef,
      {
        field: 'Manualgrade',
        headerName: '',
        sortable: false,
        width: 150,
        disableClickEventBubbling: true,
        renderCell: params => {
          const onClick = () => {
            const api: GridApi = params.api;
            const fields = api
              .getAllColumns()
              .map(c => c.field)
              .filter(c => c !== '__check__' && !!c);
            const thisRow: Record<string, GridCellValue> = {};

            fields.forEach(f => {
              thisRow[f] = params.getValue(params.id, f);
            });

            return alert(JSON.stringify(thisRow, null, 4));
          };

          return (
            <Button icon="highlight" onClick={onClick} outlined>
              Manualgrade
            </Button>
          );
        }
      } as GridColDef,
      { field: 'score', headerName: 'Score', width: 130 }
    ];
  }

  public async componentDidMount(): Promise<void> {
    const assignment: Assignment = await fetchAssignment(
      this.lectureID,
      this.assignmentID,
      false,
      true
    ).toPromise(); //TODO: Not working
    const lecture: Lecture = await getLecture(this.lectureID).toPromise();
    this.title.label = 'Grading: ' + assignment.name;
    this.setState({ assignment, lecture });
    getAllSubmissions(lecture, { id: this.assignmentID }, false).subscribe(
      async userSubmissions => {
        //{id: this.assignmentID} should be assignment
        console.log(userSubmissions);
        this.setState((this.state.submissions = userSubmissions));
        //Temp rows for testing
        this.setState((this.state.rows = this.generateRows()));
        console.log('rows:');
        console.log(this.state.rows);
      }
    );
  }

  public generateRows(): any[] {
    //let rows = [{ id: 10, user: "hasdf", date: "asdfadfa" }]
    let rows = new Array();
    //TODO: right now reading only the first
    if (this.state.option == 'latest') {
      this.state.submissions.forEach(sub => {
        //get latest submission
        let latest = sub.submissions.reduce((a, b) => {
          return new Date(a.submitted_at) > new Date(b.submitted_at) ? a : b;
        });
        rows.push({
          id: latest.id,
          name: sub.user.name,
          date: latest.submitted_at,
          status: latest.status,
          score: latest.score
        });
      });
    } else {
      this.state.submissions.forEach(sub => {
        sub.submissions.forEach(s => {
          rows.push({
            id: s.id,
            name: sub.user.name,
            date: s.submitted_at,
            status: s.status,
            score: s.score
          });
        });
      });
    }
    return rows;
  }

  public datagrid() {
    return (
      <DataGrid
        rows={this.state.rows}
        columns={this.columns}
        checkboxSelection
        disableSelectionOnClick
        onSelectionModelChange={e => {
          const selectedIDs = new Set(e);
          const selectedRowData = this.state.rows.filter(row =>
            selectedIDs.has(row.id)
          );
          this.setState({ selected: selectedRowData }, () => {
            console.log('selected rowData:', this.state.selected);
          });
        }}
      />
    );
  }

  public render() {
    const items = ['latest', 'all'];
    const buttonText = this.state.option;

    return (
      <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        {this.datagrid()}

        <StringSelect
          items={items}
          filterable={false}
          itemRenderer={this.renderSelect}
          noResults={<MenuItem disabled={true} text="No results." />}
          onItemSelect={this.handleValueChange}
        >
          <Button text={buttonText} rightIcon="caret-up" />
        </StringSelect>

        <Button
          icon="highlight"
          color="primary"
          outlined
          style={{
            alignSelf: 'flex-end',
            marginRight: '20px',
            marginBottom: '20px'
          }}
        >
          Autograde selected
        </Button>
      </div>
    );
  }

  private handleValueChange = (select: string) => {
    this.setState({ option: select }, () => {
      // you get the new value of state immediately at this callback
      this.setState((this.state.rows = this.generateRows()));
      console.log(this.state.option);
    });
  };
  private renderSelect: ItemRenderer<string> = (
    option,
    { handleClick, modifiers, query }
  ) => {
    if (!modifiers.matchesPredicate) {
      return null;
    }
    const text = option;
    return (
      <MenuItem
        active={modifiers.active}
        disabled={modifiers.disabled}
        onClick={handleClick}
        text={highlightText(text, query)}
      />
    );
  };
}

function highlightText(text: string, query: string) {
  let lastIndex = 0;
  const words = query
    .split(/\s+/)
    .filter(word => word.length > 0)
    .map(escapeRegExpChars);
  if (words.length === 0) {
    return [text];
  }
  const regexp = new RegExp(words.join('|'), 'gi');
  const tokens: React.ReactNode[] = [];
  while (true) {
    const match = regexp.exec(text);
    if (!match) {
      break;
    }
    const length = match[0].length;
    const before = text.slice(lastIndex, regexp.lastIndex - length);
    if (before.length > 0) {
      tokens.push(before);
    }
    lastIndex = regexp.lastIndex;
    tokens.push(<strong key={lastIndex}>{match[0]}</strong>);
  }
  const rest = text.slice(lastIndex);
  if (rest.length > 0) {
    tokens.push(rest);
  }
  return tokens;
}

function escapeRegExpChars(text: string) {
  return text.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, '\\$1');
}
