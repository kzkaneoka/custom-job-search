import React from "react";
import PropTypes from "prop-types";
import { Formik } from "formik";
import * as Yup from "yup";
import { Redirect } from "react-router-dom";

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
          locations: ""
        }}
        onSubmit={(values, { setSubmitting, resetForm }) => {
          props.handleSearchFormSubmit(values);
          resetForm();
          setSubmitting(false);
        }}
        validationSchema={Yup.object().shape({
          words: Yup.string().required(
            "At leaset one word is required. You can add multiple words separeated by comma."
          ),
          locations: Yup.string().required(
            "At least one location is required. You can add multiple locations separated by comma."
          )
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
                <label className="label" htmlFor="input-locations">
                  Locations
                </label>
                <input
                  name="locations"
                  id="input-locations"
                  className={
                    errors.locations && touched.locations
                      ? "input error"
                      : "input"
                  }
                  type="text"
                  placeholder="Enter locations. You can add multiple locations separeated by comma."
                  value={values.locations}
                  onChange={handleChange}
                  onBlur={handleBlur}
                />
                {errors.locations && touched.locations && (
                  <div
                    className="input-feedback"
                    data-testid="errors-locations"
                  >
                    {errors.locations}
                  </div>
                )}
              </div>
              <input
                type="submit"
                className="button is-primary"
                value="Submit"
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
