# Cloud working rules (IE/AE project work)

This repo is the cloud copy of the user's F: drive `_Claude` folders. Cloud sessions cannot see F:.

## Layout
projects/<ProjectCode>/_Claude/Handover_<ProjectCode>.md
projects/<ProjectCode>/_Claude/Agreement_Digest_<ProjectCode>.md
projects/<ProjectCode>/_Claude/text/        cached text of letters/PDFs
projects/<ProjectCode>/inputs/              letters, agreements uploaded for this work
projects/<ProjectCode>/drafts/              letters/files produced here

## Every task
- Start: read the project's Handover note (and the Digest only if a contract check is needed).
- End (automatic, don't ask): follow the work-handover-note and agreement-digest skills
  against the files above, then commit and push.
- Then send ONE sync email to the user (mailmeatpb@gmail.com) so their desktop session
  can copy the changes into F:. Format exactly:

  Subject: [Claude Sync] <ProjectCode> <YYYY-MM-DD> <short task>
  Body:
  ===HANDOVER-ADD===
  <only the new lines added to the top of the handover note>
  ===DIGEST-ADD===
  <only the new lines added to the digest's Key correspondence log, or "none">
  ===DIGEST-FULL===
  <full digest text ONLY if it was created or rebuilt in this task, else "none">
  ===DRAFTS===
  <repo paths of drafts produced; attach them if possible>
  ===END===

- Tell the user one line: "Handover note updated + sync email sent."
