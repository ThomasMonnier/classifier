import pytesseract
import streamlit as st
try:
 from PIL import Image
except ImportError:
 import Image

from langdetect import detect
from pdf2image import convert_from_path