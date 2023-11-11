import { Component, OnInit } from '@angular/core';
import { Skill } from 'src/app/shared/models/employers.model';
import UserService from 'src/app/shared/services/user.service';

@Component({
  selector: 'app-skills-list',
  templateUrl: './skills-list.component.html',
  styleUrls: ['./skills-list.component.css']
})
export class SkillsListComponent implements OnInit {

  allSkills: Skill[] = []

  constructor(private userService: UserService) { }

  ngOnInit(): void {
    this.userService.getAllSkills().subscribe((res) => {
      const items: Skill[] = res.items;
      this.allSkills = items;
    });
  }

  deleteSkill(skill: Skill) {

    this.userService.deleteSkill(skill.id).subscribe(
      res => {
        this.allSkills = this.allSkills.filter((item: Skill) => item.id != skill.id)
      }
    )

  }

}
