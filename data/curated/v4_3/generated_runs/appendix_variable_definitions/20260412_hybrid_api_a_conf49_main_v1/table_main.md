# Table Main

| Section | Variable | Field | Definition | Sample |
| --- | --- | --- | --- | --- |
| Disclosure counts | Total AI sentences per firm-year | n_total | Count of classified AI-related sentences in the firm's annual filing for year t. | Annual ever-speaker panel |
| Disclosure counts | Actionable AI sentences per firm-year | n_A | Count of AI sentences labeled actionable in year t. | Annual ever-speaker panel |
| Disclosure counts | Speculative AI sentences per firm-year | n_S | Count of AI sentences labeled speculative in year t. | Annual ever-speaker panel |
| Disclosure counts | Irrelevant AI sentences per firm-year | n_I | Count of AI sentences labeled irrelevant in year t. | Annual ever-speaker panel |
| Disclosure composition | AI focus | AI_Focus | Broad AI-disclosure intensity measure carried in the canonical panel; operationally aligned with a log(1 + AI sentence count) style intensity proxy. | Annual ever-speaker panel |
| Disclosure composition | Actionable share | share_A | Actionable AI sentences divided by total AI sentences in the firm-year. | Annual ever-speaker panel |
| Disclosure composition | Speculative share | share_S | Speculative AI sentences divided by total AI sentences in the firm-year. | Annual ever-speaker panel |
| Disclosure composition | CredAI | CredAI | Credibility-style disclosure score that increases with actionable content and decreases with speculative content; stored directly in the canonical panel. | Annual ever-speaker panel |
| Disclosure composition | A/S ratio | A_S | log((1 + actionable count) / (1 + speculative count)); higher values indicate more actionable than speculative disclosure. | Annual ever-speaker panel |
| Credibility construct | PatentMismatch | PatentMismatch | Indicator equal to one for AI-talking firm-years that are both low-credibility in disclosure (bottom yearly quartile of A_S or top yearly quartile of speculative share) and weak in contemporaneous AI patenting relative to the industry-year mean. | Annual ever-speaker panel |
| Patents | AI patents | patents_ai | Count of AI-related patents linked to the firm-year. | Annual ever-speaker panel |
| Patents | Total patents | patents_total | Count of all patents linked to the firm-year. | Annual ever-speaker panel |
| Patents | Future AI patents t+1 | log_patents_ai_lead1 | log(1 + AI patents) measured one year after the disclosure year. | Annual ever-speaker panel |
| Patents | Future AI patents t+2 | log_patents_ai_lead2 | log(1 + AI patents) measured two years after the disclosure year. | Annual ever-speaker panel |
| Controls | Log assets | ln_assets | Natural log of total assets. | Annual ever-speaker panel |
| Controls | Leverage | leverage | Debt scaled by assets. | Annual ever-speaker panel |
| Controls | Cash/assets | cash | Cash holdings scaled by assets. | Annual ever-speaker panel |
| Controls | R&D/assets | rd_intensity | Research and development expense scaled by assets. | Annual ever-speaker panel |
| Controls | CAPX/assets | capx_at | Capital expenditures scaled by assets. | Annual ever-speaker panel |
| Controls | ROA | roa | Return on assets. | Annual ever-speaker panel |
| Controls | Sales growth | sales_growth | Year-over-year sales growth rate. | Annual ever-speaker panel |
| Controls | Employees | emp | Employee count from Compustat. | Annual ever-speaker panel |
| Event-study outcomes | CAR[-1,+1] | car_m1_p1 | Cumulative abnormal return over the one-day-before to one-day-after filing window. | Filing-event sample |
| Event-study outcomes | BHAR[+2,+21] | bhar_1m | Buy-and-hold abnormal return from trading day +2 through +21 after the filing date. | Filing-event sample |
| Event-study outcomes | BHAR[+2,+63] | bhar_3m | Buy-and-hold abnormal return from trading day +2 through +63 after the filing date. | Filing-event sample |
| Event-study outcomes | BHAR[+2,+126] | bhar_6m | Buy-and-hold abnormal return from trading day +2 through +126 after the filing date. | Filing-event sample |
| Event-study outcomes | BHAR[+2,+252] | bhar_12m | Buy-and-hold abnormal return from trading day +2 through +252 after the filing date. | Filing-event sample |
| Valuation and financing | Log MktCap/assets | log_mktcap_assets | log(1 + market capitalization / assets), using merged CRSP year-end market cap and Compustat assets. | Annual panel with market merge |
| Valuation and financing | Log Q proxy | log_q_proxy | log(1 + market cap/assets + leverage), used when local pulls do not include full book-equity fields. | Annual panel with market merge |
| Valuation and financing | Delta log Q t+1 | delta_log_q_proxy_lead1 | One-year-ahead change in the log Q proxy. | Annual panel with market merge |
| Valuation and financing | Delta shares t+1 | share_growth_lead1 | Next-year growth in CRSP shares outstanding. | Annual panel with market merge |
| Valuation and financing | Issue >5% t+1 | equity_issue_lead1 | Indicator equal to one when next-year shares outstanding grow by more than 5%. | Annual panel with market merge |
| Treatment and screens | PostChatGPT | post_chatgpt / PostChatGPT | Indicator for fiscal years 2023 onward in the ChatGPT-shock designs. | Annual and event-study panels |
| Treatment and screens | Non-big screen | nonbig_marketcap | Indicator equal to one when a firm's market capitalization is at or below the matched-sample yearly median. | Annual panel with market merge |
