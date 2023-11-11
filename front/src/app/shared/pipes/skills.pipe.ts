import { Pipe, PipeTransform } from "@angular/core";

@Pipe(
    {
        name: 'skills'
    }
)
export class SkillsPipe implements PipeTransform {
    transform(skill_links: any, ...args: any[]) {
        let res = skill_links.map(
            (value: any) => value.skill
        )
        return res
    }
}