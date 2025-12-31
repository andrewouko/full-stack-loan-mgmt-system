import { useState } from "react";

export const usePagination = () => {
  const [cursor, setCursor] = useState<number | null>(null);
  const [cursorHistory, setCursorHistory] = useState<number[]>([]);

  const goToNextPage = (lastItemId: number | null) => {
    if (cursor !== null) {
      setCursorHistory((prev) => [...prev, cursor]);
    }
    setCursor(lastItemId);
  };

  const goToPreviousPage = () => {
    const newHistory = [...cursorHistory];
    const previousCursor = newHistory.pop() ?? null;
    setCursorHistory(newHistory);
    setCursor(previousCursor);
  };

  const resetPagination = () => {
    setCursor(null);
    setCursorHistory([]);
  };

  return {
    goToNextPage,
    goToPreviousPage,
    cursor,
    resetPagination,
  };
};
