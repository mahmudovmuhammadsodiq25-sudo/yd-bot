-- CreateTable
CREATE TABLE "TourImage" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "tourId" TEXT NOT NULL,
    "url" TEXT NOT NULL,
    "order" INTEGER NOT NULL DEFAULT 0,
    CONSTRAINT "TourImage_tourId_fkey" FOREIGN KEY ("tourId") REFERENCES "Tour" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- RedefineTables
PRAGMA defer_foreign_keys=ON;
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_Tour" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "title" TEXT NOT NULL,
    "slug" TEXT NOT NULL,
    "category" TEXT NOT NULL DEFAULT 'tur',
    "country" TEXT NOT NULL DEFAULT 'O''zbekiston',
    "location" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "price" INTEGER NOT NULL,
    "days" INTEGER NOT NULL,
    "imageUrl" TEXT,
    "latitude" REAL,
    "longitude" REAL,
    "featured" BOOLEAN NOT NULL DEFAULT false,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);
INSERT INTO "new_Tour" ("createdAt", "days", "description", "featured", "id", "imageUrl", "location", "price", "slug", "title", "updatedAt") SELECT "createdAt", "days", "description", "featured", "id", "imageUrl", "location", "price", "slug", "title", "updatedAt" FROM "Tour";
DROP TABLE "Tour";
ALTER TABLE "new_Tour" RENAME TO "Tour";
CREATE UNIQUE INDEX "Tour_slug_key" ON "Tour"("slug");
PRAGMA foreign_keys=ON;
PRAGMA defer_foreign_keys=OFF;
