import { useEffect, useState } from 'react';
import type { Case, CaseSummary, Document } from './types';

const unavailable = 'Unavailable in supplied evidence';
export function SourceLink({ doc }: { doc?: Document }) {
  return doc?.url?.startsWith('https://www.sec.gov/Archives/edgar/')
    ? <a href={doc.url} target="_blank" rel="noreferrer">{doc.id} ↗<span className="sr-only"> Open original SEC filing in a new tab</span></a>
    : <span className="muted">Source unavailable</span>;
}
async function getJSON<T,>(path: string, signal: AbortSignal): Promise<T> {
  const response = await fetch(path, { signal });
  if (!response.ok) throw new Error('The local evidence service could not load this view.');
  const data = await response.json();
  if (signal.aborted) throw new DOMException('Request cancelled', 'AbortError');
  return data;
}

export function CaseView({ data }: { data: Case }) {
  const [perspective, setPerspective] = useState<'equity' | 'senior_unsecured_creditor'>('equity');
  const docs = data.documents ?? [];
  return <>
    <header className="case-header">
      <div className="eyebrow">DISCLOSURE CASE <span>/ {data.ticker}</span></div>
      <h1>{data.company}</h1>
      <p className="arrangement">{data.arrangement || unavailable}</p>
      <div className="case-meta"><span>Historical cutoff <strong>{data.analysis_as_of || unavailable}</strong></span><span>{docs.length} source {docs.length === 1 ? 'document' : 'documents'}</span><span>Selected disclosure context</span></div>
    </header>
    <div className="legend" aria-label="Evidence categories">
      <span><b className="dot fact-dot" />Disclosed fact <small>Selected SEC context</small></span>
      <span><b className="dot interpretation-dot" />Conditional interpretation <small>Provisional reference</small></span>
      <span><b className="dot unknown-dot" />Unknown <small>Evidence does not establish</small></span>
    </div>
    <div className="workspace-grid">
      <div className="evidence-column">
        <section id="evidence" className="panel">
          <div className="section-heading"><div><span className="eyebrow teal">01 / DISCLOSED FACT</span><h2>Disclosure evidence</h2></div><span className="tag">Historical source pack</span></div>
          <p className="section-intro">Amounts retain their disclosed measurement and date. Contractual ceilings are distinct from recognized liabilities.</p>
          <div className="table-wrap"><table><caption className="sr-only">Disclosed amounts and their source references</caption><thead><tr><th scope="col">Measurement</th><th scope="col">Disclosed amount · USD</th><th scope="col">Source</th></tr></thead><tbody>
            {(data.amounts ?? []).map((amount) => <tr key={amount.label}><th scope="row">{amount.label}<small>{amount.context}</small></th><td className="amount">{amount.value ?? unavailable}</td><td><SourceLink doc={docs.find(doc => doc.id === amount.document_id)} /></td></tr>)}
            {!data.amounts?.length && <tr><td colSpan={3}>{unavailable}</td></tr>}
          </tbody></table></div>
          <div className="evidence-note"><strong>Evidence provenance</strong><p>Manually curated SEC quotations and paraphrases. These are selected passages, not independently certified facts or complete contracts.</p></div>
          {docs.map((doc, index) => <article className="document" key={doc.id}>
            <div className="document-top"><span className="document-number">{String(index + 1).padStart(2, '0')}</span><div><h3>{doc.title || doc.id}</h3><div className="document-meta">Filed {doc.filed_on || 'date unavailable'}{doc.period_end ? ` · Period end ${doc.period_end}` : ''}</div></div><SourceLink doc={doc} /></div>
            <p className="locator">{doc.locator || 'Locator unavailable'}</p>
            <p>{doc.factual_paraphrase || unavailable}</p>
            <details><summary>Source quotation & accession</summary>{doc.short_quote ? <blockquote>{doc.short_quote}</blockquote> : <p>Quotation unavailable</p>}<p className="mono">Accession: {doc.accession || 'Unavailable'}</p></details>
          </article>)}
          {!docs.length && <p className="empty">Source documents unavailable.</p>}
        </section>
        <section id="provenance" className="panel provenance">
          <div className="section-heading"><div><span className="eyebrow">TRACEABILITY</span><h2>Source boundaries</h2></div></div>
          <p>{data.preparation || 'Preparation notes unavailable.'}</p>
          <details><summary>Local files & integrity hashes</summary><dl><dt>Evidence pack</dt><dd>{data.evidence_file}</dd><dt>SHA-256</dt><dd className="mono">{data.evidence_sha256}</dd><dt>Provisional reference</dt><dd>{data.reference_file}</dd><dt>SHA-256</dt><dd className="mono">{data.reference_sha256}</dd></dl></details>
        </section>
      </div>
      <aside className="analysis-column" aria-label="Interpretation and limitations">
        <section id="interpretation" className="panel interpretation">
          <div className="section-heading"><div><span className="eyebrow blue">02 / CONDITIONAL INTERPRETATION</span><h2>Investor implications</h2></div></div>
          <p className="section-intro">Existing AI-assisted research reference. Provisional; independent human approval pending. These statements are interpretations, not verified disclosure facts.</p>
          <div className="perspective" role="group" aria-label="Investor perspective"><button aria-pressed={perspective === 'equity'} onClick={() => setPerspective('equity')}>Equity holder</button><button aria-pressed={perspective === 'senior_unsecured_creditor'} onClick={() => setPerspective('senior_unsecured_creditor')}>Senior unsecured creditor</button></div>
          <div className="interpretation-text" aria-live="polite"><h3>{perspective === 'equity' ? 'Equity holder' : 'Senior unsecured creditor'}</h3><p>{data.interpretations?.[perspective] || 'Interpretation unavailable in the existing reference.'}</p></div>
          <p className="footnote">Reproduced from the existing provisional reference without new inference or calculations.</p>
        </section>
        <section className="panel accounting">
          <div className="section-heading"><div><span className="eyebrow">RECOGNITION BOUNDARY</span><h2>Exposure ≠ carrying liability</h2></div></div>
          <span className={`tag ${data.accounting?.status === 'not_established' ? 'unknown-tag' : ''}`}>{data.accounting?.status === 'not_established' ? 'Carrying amount unknown' : data.accounting?.statement ? 'Recognition discussed in source pack' : 'Accounting information unavailable'}</span>
          <p>{data.accounting?.statement || unavailable}</p>
          <p className="footnote">Accounting commentary from the provisional reference; human approval pending.</p>
        </section>
        <section id="limitations" className="panel limitations">
          <div className="section-heading"><div><span className="eyebrow amber">03 / UNKNOWN OR UNSUPPORTED</span><h2>Evidence limitations</h2></div></div>
          <p className="section-intro">The existing reference identifies these boundaries. Missing evidence is never represented as zero.</p>
          {data.limitations?.length ? <ul>{data.limitations.map(item => <li key={item}>{item}</li>)}</ul> : <p>Case-specific limitations unavailable. Absence of a recorded limitation does not establish completeness.</p>}
          <div className="unknown-note">No expected-loss, default-probability or creditor-recovery estimate is supplied by this workstation.</div>
        </section>
      </aside>
    </div>
  </>;
}

export default function App() {
  const [catalog, setCatalog] = useState<CaseSummary[]>([]);
  const [selected, setSelected] = useState('nvidia-ports');
  const [data, setData] = useState<Case | null>(null);
  const [query, setQuery] = useState('');
  const [error, setError] = useState('');
  const [retry, setRetry] = useState(0);
  useEffect(() => {
    const controller = new AbortController();
    getJSON<{ cases: CaseSummary[] }>('/api/cases', controller.signal).then(result => setCatalog(result.cases)).catch(err => { if (err.name !== 'AbortError') setError(err.message); });
    return () => controller.abort();
  }, [retry]);
  useEffect(() => {
    const controller = new AbortController();
    setData(null); setError('');
    getJSON<Case>(`/api/cases/${selected}`, controller.signal).then(setData).catch(err => { if (err.name !== 'AbortError') setError(err.message); });
    return () => controller.abort();
  }, [selected, retry]);
  const filtered = catalog.filter(item => `${item.company} ${item.ticker} ${item.arrangement}`.toLowerCase().includes(query.toLowerCase()));
  return <div className="workstation">
    <a className="skip-link" href="#main">Skip to case evidence</a>
    <aside className="sidebar">
      <div className="brand"><span className="brand-mark" aria-hidden="true">∥</span><div>parallax<span>FINANCIAL EVIDENCE</span></div></div>
      <div className="sidebar-label">CASE LIBRARY <span>{catalog.length ? String(catalog.length).padStart(2, '0') : '—'}</span></div>
      <label className="search-label" htmlFor="case-search">Find a company or arrangement</label><input id="case-search" type="search" placeholder="Search cases…" value={query} onChange={event => setQuery(event.target.value)} />
      <nav aria-label="Disclosure cases" className="case-list">{filtered.map(item => <button key={item.key} className={`case-button ${selected === item.key ? 'active' : ''}`} aria-current={selected === item.key ? 'true' : undefined} onClick={() => setSelected(item.key)}><span className="case-button-top"><strong>{item.company}</strong><span className="ticker">{item.ticker}</span></span><span className="case-description">{item.arrangement}</span><span className="case-date">{item.analysis_as_of || 'Cutoff unavailable'}</span></button>)}{catalog.length > 0 && !filtered.length && <p className="empty" role="status">No matching cases. Try another company or ticker.</p>}</nav>
      <div className="sidebar-footer"><span className="local-dot" /> Local evidence workspace<p>Historical disclosures<br />Phase 1 · Read-only research</p></div>
    </aside>
    <div className="main-shell"><div className="topbar"><span>Research workstation <b>/</b> Case evidence</span><a href="#provenance">Source provenance ↓</a></div>
      <main id="main" tabIndex={-1}>{error ? <div className="panel empty" role="alert"><h1>Evidence unavailable</h1><p>{error} Check that the Python service is running on port 8001.</p><button className="retry" onClick={() => { setError(''); setRetry(value => value + 1); }}>Retry loading</button></div> : data ? <CaseView key={data.key} data={data} /> : <p className="empty" role="status">Loading disclosure evidence…</p>}</main>
      <footer className="main-footer">PARALLAX <span>Selected historical evidence · No live pricing or new inference</span></footer>
    </div>
  </div>;
}
