/** Illustrative classroom concept percentages; no assessment data is inferred. */
const competencies = [
  { label: 'Identifying fractions', percent: 85 },
  { label: 'Comparing fractions', percent: 72 },
  { label: 'Adding fractions', percent: 58 },
  { label: 'Fraction word problems', percent: 34 },
];
export default function Analytics() {
  return <div className="page narrow">
    <p className="eyebrow">TEACHER INSIGHTS · DEMO MOCKUP</p>
    <h1>Class learning analytics</h1>
    <p className="lead">Illustrative class-level competency mastery percentages. All values below are fictional demo data, not measured student performance or validated assessments.</p>
    <div className="card">
      <h2>Class competency mastery</h2>
      <p className="muted small">Mock class average · percentages are placeholders</p>
      {competencies.map(({label,percent}) => <div key={label} style={{margin:'20px 0'}}>
        <div style={{display:'flex',justifyContent:'space-between',gap:12,marginBottom:8}}><strong>{label}</strong><strong>{percent}%</strong></div>
        <div role="progressbar" aria-label={label} aria-valuenow={percent} aria-valuemin={0} aria-valuemax={100} style={{height:13,background:'#e8edf1',borderRadius:20,overflow:'hidden'}}>
          <div style={{height:'100%',width:`${percent}%`,background:percent>=80?'#709b82':percent>=60?'#b8a169':'#a17d91',borderRadius:20}} />
        </div>
      </div>)}
    </div>
    <p className="muted small">Demo only. Actual mastery analytics would require recorded assessments and an agreed scoring method.</p>
  </div>;
}
