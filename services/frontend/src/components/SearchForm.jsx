import React from "react";
import PropTypes from "prop-types";
import { Formik } from "formik";
import * as Yup from "yup";

import "./form.css";

const SearchForm = props => {
  return (
    <div>
      <h1 className="title is-1">Job Search</h1>
      <hr />
      <br />
      <Formik
        initialValues={{
          words: "",
          location: ""
        }}
        onSubmit={(values, { setSubmitting, resetForm }) => {
          props.handleSearchFormSubmit(values);
          setSubmitting(false);
        }}
        validationSchema={Yup.object().shape({
          words: Yup.string().required(
            "At leaset one word is required. You can add multiple words separeated by comma."
          ),
          location: Yup.string().required("Location is required.")
        })}
      >
        {props => {
          const {
            values,
            touched,
            errors,
            isSubmitting,
            handleChange,
            handleBlur,
            handleSubmit
          } = props;
          return (
            <form onSubmit={handleSubmit}>
              <div className="field">
                <label className="label" htmlFor="input-words">
                  Words
                </label>
                <input
                  name="words"
                  id="input-words"
                  className={
                    errors.words && touched.words ? "input error" : "input"
                  }
                  type="text"
                  placeholder="Enter words. You can add multiple words separeated by comma."
                  value={values.words}
                  onChange={handleChange}
                  onBlur={handleBlur}
                />
                {errors.words && touched.words && (
                  <div className="input-feedback" data-testid="errors-words">
                    {errors.words}
                  </div>
                )}
              </div>
              <div className="field">
                <label className="label" htmlFor="input-location">
                  Location
                </label>
                <input
                  name="location"
                  id="input-location"
                  className={
                    errors.location && touched.location
                      ? "input error"
                      : "input"
                  }
                  type="text"
                  placeholder="Enter location."
                  value={values.location}
                  onChange={handleChange}
                  onBlur={handleBlur}
                />
                {errors.location && touched.location && (
                  <div className="input-feedback" data-testid="errors-location">
                    {errors.location}
                  </div>
                )}
              </div>
              <input
                type="submit"
                className="button is-primary"
                value="Search Jobs"
                disabled={isSubmitting}
              />
            </form>
          );
        }}
      </Formik>
    </div>
  );
};

export default SearchForm;

SearchForm.propTypes = {
  handleSearchFormSubmit: PropTypes.func.isRequired
};
