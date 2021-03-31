import * as React from 'react';


export interface CoursesProps {
  courses: [];
}

export class CoursesComponent extends React.Component<CoursesProps> {
  public title: string;
  public state = {
  };

  constructor(props: CoursesProps) {
    super(props)
  }
}