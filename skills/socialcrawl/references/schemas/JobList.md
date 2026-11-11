# JobList fields

Every field the 7 field-mapped endpoints returning `JobList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `job.apply_url` | string\|null | Where to apply. Present on job detail. |
| `job.company.id` | string\|null | The employer's id on the job source. |
| `job.company.name` | string\|null | Employer name. |
| `job.company.url` | string\|null | URL of the employer's page. |
| `job.company.verified` | boolean\|null | Whether the source marks the employer as verified. |
| `job.description` | string\|null | Full job description. Present on job detail. |
| `job.easy_apply` | boolean\|null | Whether the posting can be applied to without leaving the source. |
| `job.employment_type` | string\|null | Employment type, for example Full-time or Contract. |
| `job.experience_level` | string\|null | Seniority the posting declares. Null when it declares none. |
| `job.ext.accepting_applications` | boolean\|null | Whether the posting still accepts applications. |
| `job.ext.applicant_count` | number\|null | Number of applicants so far. |
| `job.ext.board` | string\|null | The job board the posting came from. |
| `job.ext.country_code` | string\|null | Country of the job as an ISO 3166-1 alpha-2 code. |
| `job.ext.industries` | string\|null | Industry of the employer, as the posting lists it. |
| `job.ext.is_promote` | boolean\|null | Whether the posting is a paid promotion. |
| `job.ext.job_function` | string\|null | Job function the posting is filed under. |
| `job.ext.job_provider` | string\|null | The site the posting was originally listed on. |
| `job.ext.linkedin_company_name` | string\|null | The employer's company name on LinkedIn. |
| `job.ext.salary_currency` | string\|null | Currency code of salary_min and salary_max. |
| `job.ext.salary_max` | number\|null | Top of the salary range in salary_currency. The period (year, month, hour) is as the posting states it. |
| `job.ext.salary_min` | number\|null | Bottom of the salary range in salary_currency. The period (year, month, hour) is as the posting states it. |
| `job.id` | string | The job's id on its source. |
| `job.listed_at` | string\|number\|null | When the job was listed. An ISO 8601 time on most sources, but a relative label such as '4 days ago' on sources that publish no timestamp. |
| `job.location` | string\|null | Job location as the posting prints it. |
| `job.remote` | string\|null | Workplace type as the source labels it, for example Remote, Hybrid or On-site. |
| `job.title` | string\|null | Job title. |
| `job.url` | string\|null | URL of the posting. |
