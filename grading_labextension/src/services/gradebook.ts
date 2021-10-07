export class GradeBook {
    public properties: any;

    public constructor(properties: any) {
        this.properties = properties;
    }

    public setComment(notebook: string, cellId: string, comment: string) {
        this.properties["notebooks"][notebook]["comments_dict"][cellId]["manual_comment"] = comment;
    }

    public getComment(notebook: string, cellId: string): string {
        return this.properties["notebooks"][notebook]["comments_dict"][cellId]["manual_comment"];
    }

    public setManualScore(notebook: string, cellId: string, score: number) {
        this.properties["notebooks"][notebook]["grades_dict"][cellId]["manual_score"] = score;
    }

    public getManualScore(notebook: string, cellId: string): number {
        return this.properties["notebooks"][notebook]["grades_dict"][cellId]["manual_score"];
    }

    public setExtraCredit(notebook: string, cellId: string, credit: number) {
        this.properties["notebooks"][notebook]["grades_dict"][cellId]["extra_credit"] = credit;
    }

    public getExtraCredit(notebook: string, cellId: string): number {
        const extraCredit = this.properties["notebooks"][notebook]["grades_dict"][cellId]["extra_credit"];
        if (extraCredit) {
            return extraCredit;
        } else {
            return 0.0;
        }
    }

    public setNeedsManualGrading(notebook: string, cellId: string, needsGrading: boolean) {
        this.properties["notebooks"][notebook]["grades_dict"][cellId]["needs_manual_grade"] = needsGrading;
    }

    public getNeedsManualGrading(notebook: string, cellId: string): boolean {
        return this.properties["notebooks"][notebook]["grades_dict"][cellId]["needs_manual_grade"];
    }

    public getNotebookGradingInfo(notebook: string): boolean {
        const grades_dict = this.properties["notebooks"][notebook]["grades_dict"];
        return Object.keys(grades_dict).map(v => this.getNeedsManualGrading(notebook, v)).reduce((r, v) => r || v, false);
    }

    public getGradingInfo(): Map<string, boolean> {
        const map: Map<string, boolean> = new Map();
        for (let notebook of Object.keys(this.properties["notebooks"])) {
            map.set(notebook, this.getNotebookGradingInfo(notebook));
        }
        return map;
    }

    public getGradeScore(notebook: string, cellId: string): number {
        const grade = this.properties["notebooks"][notebook]["grades_dict"][cellId];
        if (grade["manual_score"] === null && grade["auto_score"] === null) {
            return 0.0;
        } else if (grade["manual_score"] === null) {
            return grade["auto_score"];
        } else if (grade["auto_score"] === null) {
            return grade["manual_score"];
        } else {
            return grade["manual_score"];
        }
    }

    public getGradeMaxScore(notebook: string, cellId: string): number {
        const grade = this.properties["notebooks"][notebook]["grades_dict"][cellId];
        if (grade["max_score_taskcell"] !== null) {
            return grade["max_score_taskcell"];
        } else if (grade["max_score_gradecell"] !== null) {
            return grade["max_score_gradecell"];
        } else {
            return 0.0;
        }
    }

    public getNotebookPoints(notebook: string): number {
        let sum: number = 0;
        const grades_dict = this.properties["notebooks"][notebook]["grades_dict"];
        for (let cellId of Object.keys(grades_dict)) {
            sum += this.getGradeScore(notebook, cellId);
        }
        return sum;
    }

    public getPoints(): number {
        let sum: number = 0;
        for (let notebook of Object.keys(this.properties["notebooks"])) {
            sum += this.getNotebookPoints(notebook);
        }
        return sum;
    }

    public getNotebookMaxPoints(notebook: string): number {
        let sum: number = 0;
        const grades_dict = this.properties["notebooks"][notebook]["grades_dict"];
        for (let cellId of Object.keys(grades_dict)) {
            sum += this.getGradeMaxScore(notebook, cellId);
        }
        return sum;
    }

    public getMaxPoints(): number {
        let sum: number = 0;
        for (let notebook of Object.keys(this.properties["notebooks"])) {
            sum += this.getNotebookMaxPoints(notebook);
        }
        return sum;
    }

    public getNotebookExtraCredit(notebook: string): number {
        let sum: number = 0;
        const grades_dict = this.properties["notebooks"][notebook]["grades_dict"];
        for (let cellId of Object.keys(grades_dict)) {
            sum += this.getExtraCredit(notebook, cellId);
        }
        return sum;
    }

    public getExtraCredits() {
        let sum: number = 0;
        for (let notebook of Object.keys(this.properties["notebooks"])) {
            sum += this.getNotebookExtraCredit(notebook);
        }
        return sum;
    }
}