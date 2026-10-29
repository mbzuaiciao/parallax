export interface CaseSummary {
  key: string; ticker: string; company: string; arrangement: string | null; analysis_as_of: string | null;
}
export interface Document {
  id: string; title?: string; accession?: string; url?: string; filed_on?: string;
  period_end?: string; locator?: string; short_quote?: string; factual_paraphrase?: string;
}
export interface Case extends CaseSummary {
  preparation?: string; documents: Document[];
  amounts: { label: string; value: string | null; document_id: string | null; context: string; status: string }[];
  evidence_file: string; evidence_sha256: string; reference_file: string; reference_sha256: string;
  reference_status: string; independent_verification?: { decision?: string };
  accounting: { status: string; statement?: string | null };
  interpretations: { status?: string; equity?: string; senior_unsecured_creditor?: string };
  limitations: string[];
}
