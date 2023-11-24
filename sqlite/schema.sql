CREATE TABLE "Hashes" (
  "Hash" TEXT,
  "Content" TEXT
);
CREATE UNIQUE INDEX "ix_Hashes_index" ON "Hashes" ("Hash");
CREATE TABLE "Projects" (
"Project_Name" TEXT,
  "Default_Branch" TEXT
);
CREATE TABLE "Authors" (
"Commit_SHA" TEXT,
  "Author_Name" TEXT,
  "Author_Email" TEXT,
  "Committer_Name" TEXT,
  "Committer_Email" TEXT
);
CREATE TABLE "Commit_Messages" (
"Commit_SHA" TEXT,
  "Commit_Message" TEXT
);
CREATE TABLE "Revisions" (
"Project_Name" TEXT,
  "File" TEXT,
  "Revision" TEXT,
  "Commit_SHA" TEXT,
  "Commit_Date" TEXT,
  "Hash" TEXT,
  "Nodes" INTEGER,
  "Edges" INTEGER
, Commit_DateTime DATETIME);
CREATE INDEX "ix_Revisions_Hashes_index" ON "Revisions" ("Hash");
CREATE INDEX "ix_Revisions_Projects_index" ON "Revisions" ("Project_Name");
CREATE INDEX "ix_Revisions_Commit_index" ON "Revisions" ("Commit_SHA");
CREATE INDEX "ix_Projects_index" ON "Projects" ("Project_Name");
CREATE INDEX "ix_Authors_index" ON "Authors" ("Commit_SHA");
CREATE INDEX "ix_Commit_Messages_Hashes_index" ON "Commit_Messages" ("Commit_SHA");
