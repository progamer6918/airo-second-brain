export type InitialRouteLike = {
  routedTo: string;
  destinationDb: string;
  reason: string;
};

export async function runFinalRouting(
  env: any,
  rawText: string,
  initialRoute: InitialRouteLike,
  recentCapturePageId: string,
  recentCaptureUrl: string
) {
  console.log("final routing helper loaded", {
    routedTo: initialRoute.routedTo,
    recentCapturePageId,
    recentCaptureUrl,
    rawLength: rawText.length,
    hasNotionToken: Boolean(env.NOTION_TOKEN),
  });

  return {
    ok: true,
    skipped: true,
    reason: "final routing helper scaffold only",
  };
}
