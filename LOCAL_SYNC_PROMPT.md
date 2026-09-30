Paste this into your regular desktop session (with the project folder added and Gmail connected):

----------------------------------------------------------------
Sync my cloud work into my project folders.

1. In Gmail, find emails with subject starting "[Claude Sync]" that do NOT have the label "Claude-Synced".
   Process them oldest first.
2. For each email, take the <ProjectCode> from the subject and use the matching project folder's
   _Claude subfolder (ask me once if the folder isn't added or the code doesn't match a folder).
3. Merge — never overwrite my own edits:
   - ===HANDOVER-ADD=== lines -> insert at the TOP of the entries in Handover_<ProjectCode>.md
     (create the file if missing). Skip any line already present.
   - ===DIGEST-ADD=== lines -> append to the "Key correspondence" log in
     Agreement_Digest_<ProjectCode>.md. Skip duplicates. Ignore if "none".
   - ===DIGEST-FULL=== -> if the digest file doesn't exist, save it as Agreement_Digest_<ProjectCode>.md.
     If it exists, do NOT replace it; save as Agreement_Digest_<ProjectCode>_cloud_<date>.md and tell me.
   - ===DRAFTS=== -> save any attachments into the project folder's Drafts (or main) folder.
4. Apply the label "Claude-Synced" to each processed email (create the label if needed).
5. Reply in one short table: project, what was added, files saved. Nothing else.
----------------------------------------------------------------
