export class GradeBook {
    public properties: any;

    public constructor(properties: any) {
        this.properties = properties;
    }

    public setComment(notebook: string, cellId: string, comment: string) {
        this.properties[notebook]["comments_dict"][cellId]["manual_comment"] = comment;
    }

    public getComment(notebook: string, cellId: string): string {
        return this.properties[notebook]["comments_dict"][cellId]["manual_comment"];
    }

    public setManualScore(notebook: string, cellId: string, score: number) {
        this.properties[notebook]["grades_dict"][cellId]["manual_score"] = score;
    }

    public getManualScore(notebook: string, cellId: string): number {
        return this.properties[notebook]["grades_dict"][cellId]["manual_score"];
    }

    public setExtraCredit(notebook: string, cellId: string, credit: number) {
        this.properties[notebook]["grades_dict"][cellId]["extra_credit"] = credit;
    }

    public getExtraCredit(notebook: string, cellId: string): number {
        return this.properties[notebook]["grades_dict"][cellId]["extra_credit"];
    }

    public setNeedsManualGrading(notebook: string, cellId: string, needsGrading: boolean) {
        this.properties[notebook]["grades_dict"][cellId]["needs_manual_grade"] = needsGrading;
    }

    public getNeedsManualGrading(notebook: string, cellId: string): boolean {
        return this.properties[notebook]["grades_dict"][cellId]["needs_manual_grade"];
    }

}