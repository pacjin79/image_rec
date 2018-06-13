import click
import glob
import os

@click.group()
def cli():
    pass

@cli.command()
def resize():
    click.echo('Resize images')

@cli.command()
@click.option('--dir', default='photo_processed', help='root director where images sit')
def rotate(dir):
    click.echo('Searching *.jpg and *.JPG files in images dir = ' + dir)
    images = glob.glob(os.path.join(dir, '**/*.jpg'), recursive=True)
    images = images + glob.glob(os.path.join(dir, '**/*.JPG'), recursive=True)
    
if __name__ == '__main__':
    cli()