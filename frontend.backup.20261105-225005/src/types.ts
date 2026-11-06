export type Role = 'student' | 'teacher';
export type Student = { id: string; name: string; interests: string[]; format: 'Pictures' | 'Written instructions' | 'Interactive'; pace: 'Small steps' | 'Medium steps'; mastery: number; completed: number; avatar: string };
export type Assignment = { id: number; title: string; studentId: string; status: 'Assigned' | 'Completed' };
