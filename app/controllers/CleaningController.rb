require "json"

class CleaningController < ApplicationController
  def new
    # Renders the form
  end

  def create
    raw_options = params.fetch(:options, {})

    uploaded = params[:file]
    sample   = raw_options["sample_csv"].presence

    if uploaded.present?
      # user uploaded a file
      upload_path = Rails.root.join("tmp", "uploads", uploaded.original_filename)
      FileUtils.mkdir_p(upload_path.dirname)
      File.binwrite(upload_path, uploaded.read)
    elsif sample.present?
      # user chose a sample CSV
      upload_path = Rails.root.join("tmp", "#{sample}.csv")
      raise "Sample file not found: #{upload_path}" unless File.exist?(upload_path)
    else
      raise "No file selected and no sample chosen"
    end

    # Test Config
    config = {
      remove_duplicates: raw_options["remove_duplicates"] == "1",
      standardize_month: raw_options["standardize_month"] == "1",
      month_column: raw_options["month_column"].presence || "month"
    }

    config_path = Rails.root.join("tmp", "config.json")
    File.write(config_path, JSON.pretty_generate(config))

    output_csv  = Rails.root.join("tmp", "outputs", "cleaned.csv")
    output_xlsx = Rails.root.join("tmp", "outputs", "cleaned.xlsx")
    FileUtils.mkdir_p(output_csv.dirname)

    python_script = Rails.root.join("lib", "assets", "python", "run_publication_cleaning.py").to_s

    success = system(
      "python3",
      python_script,
      upload_path.to_s,
      output_csv.to_s,
      output_xlsx.to_s,
      config_path.to_s
    )

    unless success && File.exist?(output_csv)
      raise "Cleaning script failed or output file missing"
    end

    require "csv"
    rows = CSV.read(output_csv, headers: true)
    @headers = rows.headers
    @preview_rows = rows.first(20)

    render :new
  end
end
