class DataController < ApplicationController

  def index
    # Just renders the button page
  end

  def run
    script1 = Rails.root.join("lib/assets/python/check_publications_cleaning.py")
    script2 = Rails.root.join("lib/assets/python/remove_duplicates.py")
    csv_path = Rails.root.join("lib/assets/python/Book2.csv")

    @check_output = `python3 #{script1} "#{csv_path}" 2>&1`
    @remove_output = `python3 #{script2} "#{csv_path}" 2>&1`

    # store results so show.html can display them
    redirect_to data_show_path(check: @check_output, remove: @remove_output)
  end

  def show
    @check_output = params[:check]
    @remove_output = params[:remove]
  end
end

