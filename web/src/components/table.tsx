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
  data: (T & { className?: string })[];
  loading: boolean;
  hasError: boolean;
  pagination?: PaginationProps;
  onRowClick?: (item: T) => void;
  actions?: React.ReactNode[];
}

export function Table<T extends Identifiable>({
  title,
  columnNames,
  data,
  loading,
  hasError,
  pagination,
  onRowClick,
  actions,
}: Readonly<Props<T>>) {
  const {
    setLimit,
    limit,
    goToNextPage,
    goToPreviousPage,
    cursor,
    pageSizeOptions,
  } = pagination || {};
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
                  className={item.className}
                >
                  {Object.values(item)
                    .filter((value) => value !== item.className)
                    .map((value, idx) => (
                      <td key={`item-${index}-${title}-value-${idx}`}>
                        {String(value)}
                      </td>
                    ))}
                </tr>
              );
            })}
            {actions && (
              <tr>
                <td colSpan={columnNames.length}>{actions}</td>
              </tr>
            )}
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
              goToNextPage(data.length > 0 ? data[data.length - 1]?.id ?? null : null);
            }}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}
