CREATE TABLE "Revisions" (
  "Project_Name" TEXT,
  "File" TEXT,
  "Revision" TEXT,
  "Commit_SHA" TEXT,
  "Commit_Date" TEXT,
  "Hash" TEXT,
  "Nodes" INTEGER,
  "Edges" INTEGER,
  "Commit_DateTime" DATETIME);
CREATE TABLE "Contents" (
  "Hash" TEXT,
  "Content" TEXT
);
CREATE UNIQUE INDEX "ix_Hashes_index" ON "Contents" ("Hash");
CREATE TABLE "Projects" (
"Project_Name" TEXT,
  "Default_Branch" TEXT,
  "Total_Commits" INTEGER
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
CREATE TABLE "Commit_Parents" (
"Commit_SHA" TEXT,
  "Parent_SHA" TEXT
);
CREATE TABLE "Content_Parents" (
"Project_Name" TEXT,
  "File" TEXT,
  "Commit_SHA" TEXT,
  "Content_Parent_SHA" TEXT
);
CREATE INDEX "ix_Revisions_Hashes_index" ON "Revisions" ("Hash");
CREATE INDEX "ix_Revisions_Projects_index" ON "Revisions" ("Project_Name");
CREATE INDEX "ix_Revisions_Commit_index" ON "Revisions" ("Commit_SHA");
CREATE INDEX "ix_Projects_index" ON "Projects" ("Project_Name");
CREATE INDEX "ix_Authors_index" ON "Authors" ("Commit_SHA");
CREATE INDEX "ix_Commit_Messages_index" ON "Commit_Messages" ("Commit_SHA");
CREATE INDEX "ix_Commit_Parents_index" ON "Commit_Parents" ("Commit_SHA");
CREATE INDEX "ix_Content_Parents_index" ON "Content_Parents" ("Commit_SHA");