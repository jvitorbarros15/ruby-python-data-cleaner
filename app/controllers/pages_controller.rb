class PagesController < ApplicationController
  def home
    our_input_text = "heart"
    @heart = `python3 lib/assets/python/heart.py "#{our_input_text}"`.strip
  end
end
