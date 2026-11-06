import { BookOpen, ClipboardCheck, Home, UserRound, Palette, LayoutDashboard, Users, ListTodo, ChartNoAxesCombined, Settings, LogOut } from 'lucide-react';
import type { Role } from '../types';
const studentItems = [{name:'Home',icon:Home},{name:'Calibration',icon:ClipboardCheck},{name:'Learn',icon:BookOpen},{name:'Profile',icon:UserRound},{name:'Avatar',icon:Palette}];
const teacherItems = [{name:'Dashboard',icon:LayoutDashboard},{name:'Students',icon:Users},{name:'Assignments',icon:ListTodo},{name:'Analytics',icon:ChartNoAxesCombined},{name:'Settings',icon:Settings}];
export default function Sidebar({role,page,onNavigate,onSignOut}:{role:Role;page:string;onNavigate:(page:string)=>void;onSignOut:()=>void}) {
  const items = role === 'student' ? studentItems : teacherItems;
  return <aside className="sidebar"><div className="brand"><span className="brand-icon">✦</span><div>Adaptive<br/>Classroom</div></div><p className="nav-label">{role.toUpperCase()} SPACE</p><nav aria-label="Main navigation">{items.map(({name,icon:Icon})=><button key={name} className={'nav-item '+(page===name?'active':'')} onClick={()=>onNavigate(name)}><Icon size={19}/>{name}</button>)}</nav><div className="sidebar-footer"><span className="demo-pill">DEMO MODE</span><button className="nav-item" onClick={onSignOut}><LogOut size={19}/> Switch view</button></div></aside>;
}
