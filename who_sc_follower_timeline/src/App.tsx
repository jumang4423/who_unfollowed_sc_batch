/* eslint-disable @typescript-eslint/no-explicit-any */
// ts ignore the whole File

import { useState, useEffect } from "react";
import "./App.css";

const toTimeline = (data: Record<string, number>) => {
  const keys = Object.keys(data);
  // sort
  keys.sort((a: string, b: string) => {
    return parseInt(a) - parseInt(b);
  });
  // reverse
  keys.reverse();
  // convert
  const timeline = keys.map((key) => {
    return {
      date: key,
      followers: data[key],
    };
  });

  return timeline;
};

function App() {
  const [timelineD, setTimelineD] = useState<
    { date: string; followers: any }[]
  >([]);
  useEffect(() => {
    fetch("/diff_cache.json")
      .then((response) => response.json())
      .then((data) => {
        setTimelineD(toTimeline(data));
      });
  }, []);
  return (
    <>
      <h1>jumang4423 follower timeline on sc</h1>
      <h3>green: followed, gray: account deleted, red: unfollowed</h3>
      <pre>
        {timelineD.map((item) => {
          return (
            <div key={item.date}>
              <div>(({item.date}))</div>
              <div>
                {item.followers.map((follower: any) => {
                  const newly_followed = follower.newly_followed; // green
                  const unfollowed = follower.unfollowed; // red
                  const account_deteled = follower.account_deleted; // yellow
                  console.log(newly_followed, unfollowed, account_deteled);
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
                        @{follower.id}
                      </a>
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </pre>
    </>
  );
}

export default App;
