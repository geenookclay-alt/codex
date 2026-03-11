export interface PolicyDecision { allowed: boolean; reasons: string[] }
export function evaluatePolicy(score:number, threshold:number): PolicyDecision {
  return score >= threshold ? { allowed: true, reasons: [] } : { allowed: false, reasons: ['below_threshold'] };
}
