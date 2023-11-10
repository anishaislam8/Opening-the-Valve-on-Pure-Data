CREATE TABLE "Projects" (
"index" INTEGER,
  "Project_Name" TEXT,
  "Default_Branch" TEXT
);
CREATE INDEX "ix_Projects_index"ON "Projects" ("index");
CREATE TABLE "Hashes" (
  "Hash" TEXT,
  "Content" TEXT
);
CREATE UNIQUE INDEX "ix_Hashes_index" ON "Hashes" ("Hash");
CREATE TABLE "Revisions" (
"index" INTEGER,
  "Project_Name" TEXT,
  "File" TEXT,
  "Revision" TEXT,
  "Commit_SHA" TEXT,
  "Commit_Date" TEXT,
  "Hash" TEXT
, Commit_DateTime DATETIME);
CREATE INDEX "ix_Revisions_index"ON "Revisions" ("index");
CREATE INDEX "ix_Revisions_Hashes_index" ON "Revisions" ("Hash");
