/* eslint-disable @typescript-eslint/no-explicit-any */

import { Button } from "@mui/joy";
import { useState, useEffect } from "react";

const toTimeline = (data: Record<string, number>) => {
  const keys = Object.keys(data);
  keys.sort((a: string, b: string) => {
    return parseInt(a) - parseInt(b);
  });
  keys.reverse();
  const timeline = keys.map((key) => {
    return {
      date: key,
      followers: data[key],
    };
  });

  return timeline;
};

const PaginationControls = ({ currentPage, totalPages, onNext, onPrev }: {
  currentPage: number;
  totalPages: number;
  onNext: () => void;
  onPrev: () => void;
}) => (
  <div style={{ margin: '1rem 0' }}>
    <Button onClick={onPrev} disabled={currentPage === 1} variant="outlined" size="sm">
      Previous
    </Button>
    <span style={{ margin: '0 1rem' }}>
      Page {currentPage} of {totalPages}
    </span>
    <Button onClick={onNext} disabled={currentPage === totalPages} variant="outlined" size="sm">
      Next
    </Button>
  </div>
);

function App() {
  const [timelineD, setTimelineD] = useState<
    { date: string; followers: any }[]
  >([]);
  const [followers_cache, setFollowersCache] = useState<Record<string, number>>({});
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 3;

  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = timelineD.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(timelineD.length / itemsPerPage);

  const nextPage = () => {
    setCurrentPage((prev) => Math.min(prev + 1, totalPages));
  };

  const prevPage = () => {
    setCurrentPage((prev) => Math.max(prev - 1, 1));
  };

  useEffect(() => {
    fetch("/diff_cache.json")
      .then((response) => response.json())
      .then((data) => {
        setTimelineD(toTimeline(data));
      });
    fetch("/followers_cache.json")
      .then((response) => response.json())
      .then((data) => {
        setFollowersCache(data);
      });
  }, []);
  return (
    <>
      <PaginationControls
        currentPage={currentPage}
        totalPages={totalPages}
        onNext={nextPage}
        onPrev={prevPage}
      />

      <pre>
        {currentItems.map((item) => {
          return (
            <div key={item.date}>
              <div>
                {(() => {
                  const [start, end] = item.date.split('_').filter(x => x.match(/^\d+$/));
                  const startDate = new Date(parseInt(end) * 1000);
                  const endDate = new Date(parseInt(start) * 1000);
                  return `${startDate.toISOString().split('T')[0]} ~ ${endDate.toISOString().split('T')[0]}`;
                })()}
              </div>
              <div>
                {item.followers.map((follower: any) => {
                  const newly_followed = follower.newly_followed;
                  const unfollowed = follower.unfollowed;
                  const account_deteled = follower.account_deleted;
                  const color = () => {
                    if (newly_followed) {
                      return "green";
                    } else if (unfollowed) {
                      return "red";
                    } else if (account_deteled) {
                      return "lightgray";
                    }
                  };
                  return (
                    <div key={follower.id}>
                      {"L "}
                      <a
                        href={`https://soundcloud.com/${follower.id}`}
                        style={{ color: color() }}
                        target="_blank"
                        rel="noreferrer"
                      >
                        @{follower.id} ({followers_cache[follower.id]})
                      </a>
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </pre>

      <PaginationControls
        currentPage={currentPage}
        totalPages={totalPages}
        onNext={nextPage}
        onPrev={prevPage}
      />
    </>
  );
}

export default App;
