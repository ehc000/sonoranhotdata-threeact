import { useState } from 'react';
import Sidebar from './components/Sidebar';
import Home from './pages/student/Home';
import Calibration from './pages/student/Calibration';
import Learn from './pages/student/Learn';
import Profile from './pages/student/Profile';
import Avatar from './pages/student/Avatar';
import Dashboard from './pages/teacher/Dashboard';
import Students from './pages/teacher/Students';
import Assignments from './pages/teacher/Assignments';
import Analytics from './pages/teacher/Analytics';
import Settings from './pages/teacher/Settings';
import { initialStudents, initialAssignments } from './data/mock';
import { useLocalState } from './hooks/useLocalState';
import type { Role, Student, Assignment } from './types';
export default function App(){
 const [role,setRole]=useState<Role|null>(null);
 const [page,setPage]=useState('Home');
 const [students,setStudents]=useLocalState<Student[]>('adaptive-demo-students',initialStudents);
 const [assignments,setAssignments]=useLocalState<Assignment[]>('adaptive-demo-assignments',initialAssignments);
 const student=students[0];
 const updateStudent=(id:string,changes:Partial<Student>)=>setStudents(prev=>prev.map(s=>s.id===id?{...s,...changes}:s));
 const chooseRole=(next:Role)=>{setRole(next);setPage(next==='student'?'Home':'Dashboard')};
 if(!role)return <div className="role-entry"><div className="role-entry-card"><div className="logo-mark">✦</div><p className="eyebrow">ADAPTIVE CLASSROOM</p><h1>How would you like to explore?</h1><p className="lead">Choose a view to explore the classroom prototype. No login needed.</p><div className="role-cards"><button className="role-card" onClick={()=>chooseRole('student')}><span>🎒</span><strong>Student</strong><small>Lessons, calibration, profile and avatar</small></button><button className="role-card" onClick={()=>chooseRole('teacher')}><span>📋</span><strong>Teacher</strong><small>Class overview, students and assignments</small></button></div><p className="muted small">Demo only — switch roles at any time.</p></div></div>;
 return <div className="app-shell"><Sidebar role={role} page={page} onNavigate={setPage} onSignOut={()=>setRole(null)}/><main className="main-content"><header className="topbar"><span>{role==='student'?'Student portal':'Teacher portal'}</span><span className="topbar-account">{role==='student'?student.avatar:'📋'} Demo view</span></header>
 {role==='student'?<>
 {page==='Home'&&<Home student={student} onNavigate={setPage}/>}
 {page==='Calibration'&&<Calibration student={student} onUpdate={changes=>updateStudent(student.id,changes)}/>}
 {page==='Learn'&&<Learn student={student} onComplete={()=>updateStudent(student.id,{mastery:Math.min(100,student.mastery+10),completed:student.completed+1})}/>}
 {page==='Profile'&&<Profile student={student} onNavigate={setPage}/>}
 {page==='Avatar'&&<Avatar student={student} onUpdate={changes=>updateStudent(student.id,changes)}/>}
 </>:<>
 {page==='Dashboard'&&<Dashboard students={students} assignments={assignments} onNavigate={setPage}/>}
 {page==='Students'&&<Students students={students} onUpdate={updateStudent}/>}
 {page==='Assignments'&&<Assignments students={students} assignments={assignments} onAdd={a=>setAssignments(prev=>[...prev,a])}/>}
 {page==='Analytics'&&<Analytics students={students}/>}
 {page==='Settings'&&<Settings/>}
 </>}
 </main></div>;
}
