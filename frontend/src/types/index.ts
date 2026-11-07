export type HazardType =
  | 'flood'
  | 'landslide'
  | 'volcano'
  | 'thunderstorm'
  | 'wind'
  | 'earthquake'
  | 'wildfire'
  | 'cyclone';

export type RiskCategory = 'low' | 'moderate' | 'high' | 'very_high' | 'extreme';

export interface LocationInfo {
  province: string;
  regency: string;
  district?: string;
  latitude: number;
  longitude: number;
}

export interface RiskScoreBreakdown {
  probability: number;
  severity: number;
  exposure: number;
  confidence: number;
  total_score: number;
  category: RiskCategory;
}

export interface DisasterEvent {
  id: string;
  hazard_type: HazardType;
  title: string;
  description: string;
  location: LocationInfo;
  severity: RiskCategory;
  risk_score: RiskScoreBreakdown;
  source: string;
  is_official_alert: boolean;
  observed_at: string;
  valid_until?: string;
  data_quality: 'verified' | 'estimated' | 'stale';
  parameters: Record<string, any>;
}

export interface DisasterAlert {
  id: string;
  hazard_type: HazardType;
  alert_level: 'advisory' | 'watch' | 'warning' | 'emergency';
  headline: string;
  instruction: string;
  affected_areas: string[];
  is_official: boolean;
  risk_score: number;
  confidence_score: number;
  source: string;
  status: string;
  issued_at: string;
  expires_at?: string;
}
