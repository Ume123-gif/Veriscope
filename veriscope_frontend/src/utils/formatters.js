export const FEATURE_MAP = {
  transaction_amount: "Transaction Amount",
  amount_deviation: "Amount Deviation",
  refund_rate: "Refund Rate",
  accounts_per_device: "Accounts per Device",
  accounts_per_ip: "Accounts per IP",
  accounts_per_card: "Accounts per Card",
  transactions_last_1h: "Transactions in Last Hour",
  transactions_last_24h: "Transactions in Last 24 Hours",
  account_age_days: "Account Age",
  refund_risk: "Refund Risk",
  device_sharing_ratio: "Device Sharing Ratio",
  ip_sharing_ratio: "IP Sharing Ratio"
};

export const formatFeatureName = (key) => FEATURE_MAP[key] || key.replace(/_/g, ' ');

export const getRiskTheme = (level) => {
  const map = {
    LOW: { text: "text-emerald-400", bg: "bg-emerald-500/10", border: "border-emerald-500/20", badge: "bg-emerald-500/20 text-emerald-300" },
    MEDIUM: { text: "text-amber-400", bg: "bg-amber-500/10", border: "border-amber-500/20", badge: "bg-amber-500/20 text-amber-300" },
    HIGH: { text: "text-rose-400", bg: "bg-rose-500/10", border: "border-rose-500/20", badge: "bg-rose-500/20 text-rose-300" },
    CRITICAL: { text: "text-red-500", bg: "bg-red-500/10", border: "border-red-500/20", badge: "bg-red-500/20 text-red-300" },
  };
  return map[level?.toUpperCase()] || map.LOW;
};

export const getDecisionTheme = (decision) => {
  const map = {
    ALLOW: { border: "border-emerald-500/30", bg: "bg-emerald-950/20", text: "text-emerald-400", sub: "Transaction clears all automated security layers." },
    REVIEW: { border: "border-amber-500/30", bg: "bg-amber-950/20", text: "text-amber-400", sub: "Manual review required: Statistical variance detected." },
    HOLD: { border: "border-orange-500/30", bg: "bg-orange-950/20", text: "text-orange-400", sub: "Temporarily held for security baseline verification." },
    BLOCK: { border: "border-rose-500/30", bg: "bg-rose-950/20", text: "text-rose-400", sub: "Hard block triggered: High-probability syndicate pattern." }
  };
  return map[decision?.toUpperCase()] || { border: "border-radar-700", bg: "bg-radar-850", text: "text-slate-300", sub: "Status evaluation unavailable." };
};