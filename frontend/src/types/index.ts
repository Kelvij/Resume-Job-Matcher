export type SkillStatus = 'matched' | 'partial' | 'missing'

export interface SkillItem {
  skill: string
  status: SkillStatus
  evidence?: string | null
}

export interface PreferredSkill {
  skill: string
  matched: boolean
  evidence?: string | null
}

export interface ProjectItem {
  name: string
  relevance_score: number
  level: 'High' | 'Medium' | 'Low'
  reasons: string[]
  evidence?: string | null
}

export interface ScoreComponent {
  score: number
  weight: number
  contribution: number
}

export interface Report {
  overall_score: number
  score_components: Record<string, ScoreComponent>
  matched_skills: SkillItem[]
  partial_skills: SkillItem[]
  missing_skills: SkillItem[]
  preferred_skills: PreferredSkill[]
  skill_summary: {
    matched_count: number
    partial_count: number
    missing_count: number
  }
  job_requirements: {
    required_skills: string[]
    preferred_skills: string[]
    tools_technologies: string[]
    education_requirements: string[]
    experience_years?: number | null
    soft_skills: string[]
    domain_requirements: string[]
  }
  resume_analysis: {
    technical_skills: string[]
    programming_languages: string[]
    frameworks: string[]
    tools: string[]
    education: { text: string; terms: string[] }
    experience: { text: string; years?: number | null }
    certifications: string[]
    achievements: string[]
  }
  project_relevance: ProjectItem[]
  experience_alignment: {
    resume_years?: number | null
    required_years?: number | null
    score: number
    explanation: string
  }
  skill_gap_analysis: {
    high_priority: { priority: string; skill: string; why_it_matters: string }[]
    low_priority: { priority: string; skill: string; why_it_matters: string }[]
  }
  recommendations: {
    action: string
    basis: string
    evidence_type: string
    evidence?: string | null
  }[]
  semantic_evidence: {
    resume_to_jd_similarity: number
    note: string
  }
  llm_enrichment?: {
    executive_summary?: string
    recommendation_explanations?: string[]
    rewritten_bullets?: { original?: string; rewritten?: string; rationale?: string }[]
    status?: string
    message?: string
  }
}

export interface Analysis {
  id?: string | null
  demo?: boolean
  resume_name: string
  company_name?: string | null
  job_title?: string | null
  report: Report
}

export interface HistoryItem {
  id: string
  resume_name: string
  company_name?: string | null
  job_title?: string | null
  score: number
  created_at: string
}
