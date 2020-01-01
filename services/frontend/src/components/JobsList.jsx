import React from "react";
import PropTypes from "prop-types";

const JobsList = props => {
  return (
    <div>
      <table className="table is-hoverable is-fullwidth">
        <thead>
          <tr>
            <th>Company</th>
            <th>Job Title</th>
            <th>Location</th>
            <th>Posted Date</th>
            <th>Link</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {props.jobs.map(job => {
            return (
              <tr key={job.link}>
                <td>{job.company}</td>
                <td>{job.title}</td>
                <td>{job.location}</td>
                <td>{job.date}</td>
                <td>{job.link}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

JobsList.propTypes = {
  jobs: PropTypes.array.isRequired
};

export default JobsList;
