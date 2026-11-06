import type { Student, Assignment } from '../types';
export const initialStudents: Student[] = [
  {id:'s1',name:'Alex Rivera',interests:['3D printing','Animals'],format:'Pictures',pace:'Small steps',mastery:40,completed:3,avatar:'🦊'},
  {id:'s2',name:'Sam Lee',interests:['Space','Robots'],format:'Interactive',pace:'Small steps',mastery:68,completed:5,avatar:'🚀'},
  {id:'s3',name:'Jordan Park',interests:['Drawing','Music'],format:'Written instructions',pace:'Medium steps',mastery:75,completed:7,avatar:'🎨'},
];
export const initialAssignments: Assignment[] = [{id:1,title:'Fractions: Equal Parts',studentId:'s1',status:'Assigned'},{id:2,title:'Fractions: Equal Parts',studentId:'s2',status:'Completed'}];
export const lessonSteps = ['A fraction represents part of a whole.','Imagine dividing a 3D-printed cube into two equal pieces.','One of those two equal pieces represents one-half.'];
