# JobList fields

Every field the 7 field-mapped endpoints returning `JobList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `job.apply_url` | string\|null |  |
| `job.company.id` | string\|null |  |
| `job.company.name` | string\|null |  |
| `job.company.url` | string\|null |  |
| `job.company.verified` | boolean\|null |  |
| `job.description` | string\|null |  |
| `job.easy_apply` | boolean\|null |  |
| `job.employment_type` | string\|null |  |
| `job.experience_level` | string\|null |  |
| `job.ext.accepting_applications` | boolean\|null |  |
| `job.ext.applicant_count` | number\|null |  |
| `job.ext.board` | string\|null |  |
| `job.ext.country_code` | string\|null |  |
| `job.ext.industries` | string\|null |  |
| `job.ext.is_promote` | boolean\|null |  |
| `job.ext.job_function` | string\|null |  |
| `job.ext.job_provider` | string\|null |  |
| `job.ext.linkedin_company_name` | string\|null |  |
| `job.ext.salary_currency` | string\|null |  |
| `job.ext.salary_max` | number\|null |  |
| `job.ext.salary_min` | number\|null |  |
| `job.id` | string |  |
| `job.listed_at` | string\|number\|null |  |
| `job.location` | string\|null |  |
| `job.remote` | string\|null |  |
| `job.title` | string\|null |  |
| `job.url` | string\|null |  |
