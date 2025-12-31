import { isValidElement, ReactNode } from "react";

interface Identifiable {
  id: number;
}

interface PaginationProps {
  setLimit: (limit: number) => void;
  limit: number;
  goToNextPage: (lastItemId: number | null) => void;
  goToPreviousPage: () => void;
  cursor: number | null;
  pageSizeOptions: number[];
  totalItems: number;
  nextCursor: number | null;
}

interface Props<T extends Identifiable> {
  title: string;
  columnNames: string[];
  data: T[];
  loading: boolean;
  hasError: boolean;
  pagination?: PaginationProps;
  onRowClick?: (item: T) => void;
}

export function Table<T extends Identifiable>({
  title,
  columnNames,
  data,
  loading,
  hasError,
  pagination,
  onRowClick,
}: Readonly<Props<T>>) {
  const {
    setLimit,
    limit,
    goToNextPage,
    goToPreviousPage,
    cursor,
    pageSizeOptions,
  } = pagination || {};

  const renderCellValue = (value: unknown): ReactNode => {
    if (isValidElement(value)) {
      return value;
    }
    if (value === null || value === undefined) {
      return "";
    }
    if (
      typeof value === "string" ||
      typeof value === "number" ||
      typeof value === "boolean"
    ) {
      return String(value);
    }
    return "";
  };

  return (
    <div>
      {pagination && setLimit && pageSizeOptions && (
        <div className="pagination-controls">
          <label>
            <p>{title} per page:</p>
            <select
              value={limit}
              onChange={(e) => setLimit(Number(e.target.value))}
            >
              {pageSizeOptions.map((size) => (
                <option key={size} value={size}>
                  {size}
                </option>
              ))}
            </select>
          </label>
        </div>
      )}
      {data.length ? (
        <table className="loans-table">
          <thead>
            <tr>
              {columnNames.map((colName, idx) => (
                <th key={`header-${idx}-${title}`}>{colName}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((item, index) => {
              return (
                <tr
                  key={`item-${index}-${title}`}
                  onClick={() => onRowClick?.(item)}
                >
                  {Object.values(item).map((value, idx) => (
                    <td key={`item-${index}-${title}-value-${idx}`}>
                      {renderCellValue(value)}
                    </td>
                  ))}
                </tr>
              );
            })}
          </tbody>
        </table>
      ) : (
        <div>No data</div>
      )}
      {pagination && goToPreviousPage && goToNextPage && limit && (
        <div className="pagination-buttons">
          <button
            disabled={!cursor || loading || hasError}
            onClick={goToPreviousPage}
          >
            Previous
          </button>
          <button
            disabled={pagination.nextCursor === null || loading || hasError}
            onClick={() => {
              goToNextPage(
                data.length > 0 ? data[data.length - 1]?.id ?? null : null
              );
            }}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}
